import boto3
import os
import re
from .common import *

FROM_ADDRESS = os.environ['FROM_ADDRESS']
EMAIL_SUBJECT = os.environ['EMAIL_SUBJECT']
EMAIL_BODY = os.environ['EMAIL_BODY']
USERNAME_REGEX = re.compile(os.environ['USERNAME_REGEX'])


def handler(evt, ctx):
    print(f'Received event: {evt}')

    account_id = ctx.invoked_function_arn.split(":")[4]

    for r in evt['Records']:
        email = r['ses']['mail']['source']

        iam = boto3.client('iam')
        new_password = generate_password(iam)

        # Set the password
        print(f'Resetting password for {email}')
        iam.update_login_profile(
            UserName=email,
            Password=new_password,
            PasswordResetRequired=True,
        )

        data = {
            'login_link': f'https://{account_id}.signin.aws.amazon.com/console',
            'email': email,
            'password': new_password,
        }
        send_email_notification(FROM_ADDRESS, email, EMAIL_SUBJECT, EMAIL_BODY, data)
