import argparse
import asyncio
import logging
import time

import boto3
import docker
from botocore.exceptions import ClientError

LOG = logging.getLogger(__name__)


# python main.py --docker-image python --bash-command $'pip install pip -U && pip
# install tqdm && python -c \"import time\ncounter = 0\nwhile
# True:\n\tprint(counter)\n\tcounter = counter + 1\n\ttime.sleep(0.1)\"'
# --aws-cloudwatch-group test-task-group-1 --aws-cloudwatch-stream test-task-stream-1
# --aws-access-key-id ... --aws-secret-access-key ... --aws-region ...

class AwsApi:
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_cloudwatch_stream, aws_cloudwatch_group,
                 aws_region):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_cloudwatch_stream = aws_cloudwatch_stream
        self.aws_cloudwatch_group = aws_cloudwatch_group
        self.aws_region = aws_region
        self.client = boto3.client('logs', region_name=aws_region, aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key)
        self.retention_period_in_days = 1

    def __enter__(self):
        try:
            self.check_or_create_cloudwatch()
        except ClientError:
            LOG.error(f"Can't init connection to aws cloud watch\n{'=' * 80}", exc_info=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            try:
                self.clean_up()
            except ClientError:
                LOG.error(f"Can't clean up aws cloud watch\n{'=' * 80}", exc_info=True)

    def check_or_create_cloudwatch(self):
        if not self.does_group_exists():
            self.client.create_log_group(
                logGroupName=self.aws_cloudwatch_group,
                tags={
                    'RetentionPeriod': str(self.retention_period_in_days)
                }
            )

        if not self.does_log_stream_exists():
            self.client.create_log_stream(
                logGroupName=self.aws_cloudwatch_group,
                logStreamName=self.aws_cloudwatch_stream
            )

    def does_group_exists(self):
        response = self.client.describe_log_groups(logGroupNamePrefix=self.aws_cloudwatch_group)
        for each_line in response['logGroups']:
            if self.aws_cloudwatch_group == each_line['logGroupName']:
                return True

    def does_log_stream_exists(self):
        response = self.client.describe_log_streams(
            logStreamNamePrefix=self.aws_cloudwatch_stream
        )
        for each_line in response['logStreams']:
            if self.aws_cloudwatch_stream == each_line['logGroupName']:
                return True

    def send_log(self, log_msg):
        self.client.put_log_events(
            logGroupName=self.aws_cloudwatch_group,
            logStreamName=self.aws_cloudwatch_stream,
            logEvents=[
                {
                    'timestamp': int(round(time.time() * 1000)),
                    'message': log_msg
                }
            ]
        )

    def clean_up(self):
        self.client.delete_log_group(
            logGroupName=self.aws_cloudwatch_group
        )


class DockerRun:
    def __init__(self, docker_image, bash_command):
        self.client = docker.from_env()
        self.log_generator = self.client.containers.run(docker_image, f'sh -c \'{bash_command}\'',
                                                        auto_remove=False,
                                                        detach=True, stream=True)

    def __iter__(self):
        # on one iteration always return <= 16384 bytes
        return self.log_generator.logs(stream=True, stdout=True, stderr=True)


def parse_args():
    parser = argparse.ArgumentParser(
        prog='Test Task',
        description='Task that test me')

    parser.add_argument('--docker-image', required=True, help='docker image name')
    parser.add_argument('--bash-command', required=True, help='bash command to run inside docker container')
    parser.add_argument('--aws-cloudwatch-group', required=True, help='name of an AWS CloudWatch group')
    parser.add_argument('--aws-cloudwatch-stream', required=True, help='name of an AWS CloudWatch stream')
    parser.add_argument('--aws-access-key-id', required=True, help='AWS access key id')
    parser.add_argument('--aws-secret-access-key', required=True, help='AWS secret access key')
    parser.add_argument('--aws-region', default='us-west-1', help='name of an AWS region')

    return parser.parse_args()


async def main(args):
    docker_run = DockerRun(args.docker_image, args.bash_command)
    with AwsApi(
            aws_access_key_id=args.aws_access_key_id,
            aws_secret_access_key=args.aws_secret_access_key,
            aws_cloudwatch_stream=args.aws_cloudwatch_stream,
            aws_cloudwatch_group=args.aws_cloudwatch_group,
            aws_region=args.aws_region
    ) as aws_api:
        try:
            for log_line in docker_run:
                aws_api.send_log(log_line)
        except KeyboardInterrupt:
            return


if __name__ == "__main__":
    asyncio.run(main(parse_args()))
