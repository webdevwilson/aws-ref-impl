# spa-canary-deploy

Creates a SPA application

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
    --stack-name <STACK NAME> \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides \
        SiteId=<VALUE> \
        DomainName=<VALUE>
```

### Parameters

* **SiteId** - Unique (to your account) ID of the site
* **DomainName** - The domain name associated with this site