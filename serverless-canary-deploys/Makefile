SAM_PKG_TEMPLATE := dist/deploy.pkg.yaml
SAM_STACK_NAME := sls-canary-deploy
SAM_TEMPLATE := deploy.yaml

clean:
	rm -rf dist

dist:
	mkdir dist

$(SAM_PKG_TEMPLATE): dist
	aws cloudformation package \
		--template-file $(SAM_TEMPLATE) \
		--s3-bucket $(S3_BUCKET) \
		--output-template-file $(SAM_PKG_TEMPLATE)

deploy: $(SAM_PKG_TEMPLATE)
	aws cloudformation deploy \
		--template-file $(SAM_PKG_TEMPLATE) \
		--stack-name $(SAM_STACK_NAME) \
		--capabilities CAPABILITY_IAM \
		--parameter-overrides \
			VersionParameter=$(VERSION) \
			AliasParameter=live