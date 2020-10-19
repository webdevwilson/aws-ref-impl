import boto3
import os
import re

from .common import *

FROM_ADDRESS = os.environ['FROM_ADDRESS']
EMAIL_SUBJECT = os.environ['EMAIL_SUBJECT']
EMAIL_BODY = os.environ['EMAIL_BODY']
USERNAME_REGEX = re.compile(os.environ['USERNAME_REGEX'])


def handler(evt, _):
    print(f'Received event: {evt}')

    # Email address is the username
    email = evt['detail']['requestParameters']['userName']

    # Only configure users that match the regex
    if not USERNAME_REGEX.match(email):
        print(f'Skipping user {email}')
        return

    iam = boto3.client('iam')
    password = generate_password(iam)

    # Set the password
    print(f'Creating login for {email}')
    iam.create_login_profile(
        UserName=email,
        Password=password,
        PasswordResetRequired=True,
    )

    # Create the content of the email with templating
    account_id = evt['account']
    data = {
        'login_link': f'https://{account_id}.signin.aws.amazon.com/console',
        'email': email,
        'password': password,
    }
    ses = boto3.client('sesv2')
    send_email_notification(ses, FROM_ADDRESS, email, EMAIL_SUBJECT, EMAIL_BODY, data)
