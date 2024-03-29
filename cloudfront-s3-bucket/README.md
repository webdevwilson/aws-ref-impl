# cloudfront-s3-bucket

Creates a CloudFront distribution in front of a private S3 bucket using an origin access identity to access the bucket. Uses certificate created in ACM. Useful for hosting static websites in S3.

## Certificate

DNS validation will need to be completed while the stack update is in process. Copy the value available from CloudFormation console during the update and add to your DNS records.

## Usage

* simple-public - Cheapest setup, host site with S3 bucket and nothing else
* cloudfront-public - Adds Cloudfront distribution for hosting the site for less latency
* cloudfront-auth - Adds BASIC Authentication for protected content 
* full - Configure CloudFront, ACM, Route53

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
    --stack-name <STACK NAME> \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides \
        SiteId=<VALUE> \
        DomainName=<VALUE>
```

### Parameters

* **SiteId** - Unique (to your account) ID of the site
* **DomainName** - The domain name associated with this site