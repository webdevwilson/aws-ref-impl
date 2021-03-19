# lambda-expire-cloudwatch-logs

Schedule to run daily to set the retention policy on all cloudwatch log groups.

## How to use

The lambda is triggered by a scheduled cloudwatch event. The log retention policies are
specified in the input for the event.

The following policy sets a default retention of 90. The default policy must be the last policy
in the list of policies.

```json
{
    "Policies": [{
        "logGroupNamePrefix": "/aws/codebuild",
        "logRetentionInDays": 14
    }, {
        "logGroupNamePrefix": "/aws/lambda",
        "logRetentionInDays": 30
    }, {
        "logRetentionInDays": 90
    }]
}
```

## Deploy

```shell script
aws cloudformation package --template-file template.yml --s3-bucket <YOUR S3 BUCKET> --output-template-file template.pkg.yml
```

```shell script
aws cloudformation deploy --template-file template.pkg.yml --stack-name <YOUR STACK NAME> --capabilities CAPABILITY_IAM
```
