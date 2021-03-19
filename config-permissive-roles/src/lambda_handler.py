import boto3
import os

iam = boto3.client('iam')
cloudtrail = boto3.client('cloudtrail')

CLOUDTRAIL_NAME = os.environ.get('CLOUDTRAIL_NAME', 'PermissiveRolesCloudTrail')

def handler(_,__):
    
    # Scan roles
    roles = iam.get_paginator('list_roles')
    for page in roles.paginate():
        for role in page['Roles']:
            check_role(role['RoleName'], role['Arn'])

    # Scan users


def check_role(name, arn):
    resp = cloudtrail.lookup_events(
        LookupAttributes=[{
            'AttributeKey': 'Username',
            'AttributeValue': arn
        }]
    )

    print(name)

if __name__ == '__main__':
    handler(None, None)