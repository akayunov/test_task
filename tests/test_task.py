import time
from unittest.mock import ANY

import pytest

from task import main
from .fixtures.boto3_mock import Boto3ClientMock


@pytest.mark.asyncio
async def test_task(main_args, start_time):
    await main.main(main_args)
    assert Boto3ClientMock.logs == {'task': {'task': [[{'message': b'0\n', 'timestamp': ANY}],
                                                      [{'message': b'1\n', 'timestamp': ANY}],
                                                      [{'message': b'2\n', 'timestamp': ANY}],
                                                      [{'message': b'3\n', 'timestamp': ANY}],
                                                      [{'message': b'4\n', 'timestamp': ANY}],
                                                      [{'message': b'5\n', 'timestamp': ANY}],
                                                      [{'message': b'6\n', 'timestamp': ANY}],
                                                      [{'message': b'7\n', 'timestamp': ANY}],
                                                      [{'message': b'8\n', 'timestamp': ANY}],
                                                      [{'message': b'9\n', 'timestamp': ANY}]]}}

    assert all(
        start_time <= log['timestamp'] / 1000 <= time.time() for logs in Boto3ClientMock.logs['task']['task'] for log in
        logs)
