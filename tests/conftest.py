import os
import sys
import time
from argparse import Namespace

import pytest

from .fixtures import boto3_mock

root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(root_dir, 'src'))

sys.modules['boto3'] = boto3_mock

TEST_RUN_START_TIME = None


@pytest.fixture(autouse=True)
def start_time():
    global TEST_RUN_START_TIME
    if not TEST_RUN_START_TIME:
        TEST_RUN_START_TIME = time.time()
    yield TEST_RUN_START_TIME


@pytest.fixture
def main_args():
    return Namespace(
        docker_image='task',
        bash_command='python /tmp/script.py',
        aws_cloudwatch_group='task',
        aws_cloudwatch_stream='task',
        aws_access_key_id='task',
        aws_secret_access_key='task',
        aws_region='task'
    )
