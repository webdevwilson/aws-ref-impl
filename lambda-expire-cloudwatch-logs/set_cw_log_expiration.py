#!/usr/bin/env python3
import boto3

def handler(_, __):
    cloudwatch = boto3.client('cloudwatch')
    pass