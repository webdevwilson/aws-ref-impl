# codepipeline-hugo-site

Creates a pipeline in CodePipeline that builds a site with hugo and uploads it to S3. Sample buildspec is included and should be placed in the root of the repository.

# Usage

## Package

This template uses the serverless transform. As such you will need to package it first:

```
aws cloudformation package \
	 	--template-file template.yaml \
	 	--output-template-file template.pkg.yaml \
		--s3-bucket <S3 BUCKET FOR LAMBDA CODE>
```

## Deploy

The following command can be used to deploy the template. You must provide an ID and domain name for the template parameters.

```
aws cloudformation deploy \
    --template-file template.pkg.yaml \
    --stack-name <STACK NAME> \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides \
        ArtifactBucketName=<VALUE> \
        CloudFrontDistributionId=<VALUE> \
        DomainName=<VALUE> \
        GitHubAuthToken=<VALUE> \
        GitHubOwner=<VALUE> \
        GitHubRepo=<VALUE> \
        SiteId=<VALUE> \
        WebBucketName=<VALUE>
```

### Parameters

* **ArtifactBucketName** - Bucket CodePipeline uses to place build artifacts
* **CloudFrontDistributionId** - ID of the CloudFront distribution associated with this site
* **GitHubAuthToken** - Auth token used to connect to Github ([Help](https://docs.aws.amazon.com/codepipeline/latest/userguide/GitHub-create-personal-token-CLI.html))
* **GitHubOwner** - Team or owner of the GH repo
* **GitHubRepo** - Name of the GH repo
* **SiteId** - Unique ID of the site
* **WebBucketName** - Bucket the site files will be placed in
