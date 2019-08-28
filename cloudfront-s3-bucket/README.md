# cloudfront-s3-bucket

Creates a CloudFront distribution in front of a private S3 bucket using an origin access identity to access the bucket. Uses certificate created in ACM. Useful for hosting static websites in S3.

## Certificate

DNS validation will need to be completed while the stack update is in process. Copy the value available from CloudFormation console during the update and add to your DNS records.

## Usage

### Package

This template uses the serverless transform. As such you will need to package it first:

```
aws cloudformation package \
	 	--template-file template.yaml \
	 	--output-template-file template.pkg.yaml \
		--s3-bucket <S3 BUCKET FOR LAMBDA CODE>
```

### Deploy

The following command can be used to deploy the template. You must provide an ID and domain name for the template parameters.

```
aws cloudformation deploy \
    --template-file template.pkg.yaml \
    --stack-name s3-bucket-site \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides \
        SiteId=<SITE_ID> \
        DomainName=<DOMAIN NAME>
```