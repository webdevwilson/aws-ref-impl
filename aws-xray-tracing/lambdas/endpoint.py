import json
import boto3
import os

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch
patch(['boto3'])

QUEUE_URL = os.environ['QUEUE_URL']


def handler(evt, _):
    print(json.loads(evt['body']))
    with xray_recorder.in_subsegment('Process') as _:
        boto3.client('sqs').send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=evt['body'],
        )
    return {
        'statusCode': 200,
        'body': 'OK',
    }
