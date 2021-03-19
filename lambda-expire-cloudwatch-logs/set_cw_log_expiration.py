#!/usr/bin/env python3
import boto3

DEFAULT_RETENTION = 90


def handler(evt, __):

    print(f'Received event: {evt}')
    logs = boto3.client('logs')
    paginator = logs.get_paginator('describe_log_groups')

    if 'Policies' not in evt:
        print(f'Using default retention of {DEFAULT_RETENTION} days on all log groups')
        policies = [{}]
    else:
        policies = evt['Policies']

    # This will be used to track the log groups that have been updated, so they
    # are not updated multiple times (ie. by the default rule)
    track_log_groups = []

    for policy in policies:

        # Get log group prefix from the event
        log_group_prefix = policy.get('logGroupNamePrefix', '')
        if log_group_prefix == '':
            args = {}
        else:
            args = {'logGroupNamePrefix': log_group_prefix}

        # Get the retention policy from the event
        retention_policy = int(policy.get('logRetentionInDays', DEFAULT_RETENTION))

        # Loop through groups and update accordingly
        for page in paginator.paginate(**args):
            for log_group in page['logGroups']:
                name = log_group['logGroupName']
                retention = log_group.get('retentionInDays', -1)
                print(f'Checking log group {name}, current retention {retention}')
                if name not in track_log_groups and retention != retention_policy:
                    print(f"Changing retention on log group {name} from {retention} to {retention_policy}")
                    logs.put_retention_policy(
                        logGroupName=name,
                        retentionInDays=retention_policy,
                    )
                track_log_groups.append(name)

