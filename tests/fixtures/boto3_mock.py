class Boto3ClientMock:
    # init state
    logGroupName = []
    logs = {}

    def __init__(self, service, region_name, aws_access_key_id, aws_secret_access_key):
        self.service = service
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def create_log_group(self, logGroupName, tags):
        self.logGroupName.append(logGroupName)

    def create_log_stream(self, logGroupName, logStreamName):
        ...

    def describe_log_groups(self, logGroupNamePrefix):
        return {
            'logGroups': [log_group_name for log_group_name in self.logGroupName if
                          log_group_name.startswith(logGroupNamePrefix)]
        }

    def describe_log_streams(self, logStreamNamePrefix):
        return {
            'logStreams': []
        }

    def put_log_events(self, logGroupName, logStreamName, logEvents):
        if logGroupName not in self.logs or logStreamName not in self.logs[logGroupName]:
            self.logs[logGroupName] = {logStreamName: []}
        self.logs[logGroupName][logStreamName].append(logEvents)

    def delete_log_group(self, logGroupName):
        ...


def client(*args, **kwargs):
    return Boto3ClientMock(*args, **kwargs)
