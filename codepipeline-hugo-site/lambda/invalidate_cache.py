import boto3
import json
import os
import time;

cloudfront = boto3.client('cloudfront')
codepipeline = boto3.client('codepipeline')
DISTRIBUTION_ID = os.environ.get('DISTRIBUTION_ID')

def handler(event, context):
    print("Event: %s" % json.dumps(event))
    job_id = event['CodePipeline.job']['id']
    try:
        print("Invalidating cache for distribution \'%s\'" % DISTRIBUTION_ID)
        resp = cloudfront.create_invalidation(
            DistributionId=DISTRIBUTION_ID,
            InvalidationBatch={
                'Paths': {
                    'Quantity': 1,
                    'Items': [
                        '/*',
                    ]
                },
                'CallerReference': str(time.time())
            }
        )
        print('Response: %s' % resp)
        codepipeline.put_job_success_result(jobId=job_id)
    except Exception as e:
        codepipeline.put_job_failure_result(jobId=job_id, failureDetails={'message': e, 'type': 'JobFailed'})