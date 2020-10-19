import boto3
import random
import string


def generate_password(iam):
    """ Generates a password for the user"""

    resp = iam.get_account_password_policy()

    password_length = resp['MinimumPasswordLength']

    # Create random password
    symbols = string.ascii_letters + string.digits + '@_!-$^&*()'
    return ''.join(random.choice(symbols) for i in range(password_length))


def send_email_notification(ses, from_address, to_address, subject, body, data):
    email_subject = subject.format_map(data)
    email_body = body.format_map(data)

    # Send the email to the user
    print(f'Sending email \'{email_subject}\' to {to_address}')
    ses.send_email(
        FromEmailAddress=from_address,
        Destination={
            'ToAddresses': [to_address],
        },
        Content={
            'Simple': {
                'Subject': {
                    'Data': email_subject,
                },
                'Body': {
                    'Text': {
                        'Data': email_body,
                    },
                }
            }
        }
    )

