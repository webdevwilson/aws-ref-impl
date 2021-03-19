from aws_xray_sdk.core import patch, xray_recorder
import boto3
import os
from random import *

patch(['boto3'])

S3_BUCKET = os.environ['S3_BUCKET']


@xray_recorder.capture('Handler')
def handler(evt, _):
    print(evt)
    if randint(0, 9) >= 8:
        raise Exception('Fails 20% of the time')
    else:
        boto3.client('s3').put_object(
            ACL='private',
            Key='message.json',
            Body=bytes(evt['Records'][0]['Sns']['Message'], 'utf-8'),
            Bucket=S3_BUCKET,
        )
