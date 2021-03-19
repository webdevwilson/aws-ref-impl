from aws_xray_sdk.core import patch, xray_recorder
import boto3
import os
from random import *

patch(['boto3'])

TOPIC_ARN = os.environ['TOPIC_ARN']


def handler(evt, _):
    records = evt['Records']
    for r in records:
        process_record(r)


@xray_recorder.capture('Process Message')
def process_record(record):
    if randint(0, 9) >= 8:
        raise Exception('Fail 20% of the time')
    else:
        boto3.client('sns').publish(
            TopicArn=TOPIC_ARN,
            Message=record['body'],
        )
