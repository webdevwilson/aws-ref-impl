INFRA_PKG_TEMPLATE := dist/infrastructure.pkg.yaml
INFRA_STACK_NAME := spa-canary-deploy
INFRA_TEMPLATE := cfn/infrastructure.yaml

clean:
	rm -rf dist

dist:
	mkdir dist

$(INFRA_PKG_TEMPLATE): dist
	aws cloudformation package \
		--template-file $(INFRA_TEMPLATE) \
		--s3-bucket $(S3_BUCKET) \
		--output-template-file $(INFRA_PKG_TEMPLATE)

deploy-infrastructure: $(INFRA_PKG_TEMPLATE)
	aws cloudformation deploy \
		--template-file $(INFRA_PKG_TEMPLATE) \
		--stack-name $(INFRA_STACK_NAME) \
		--capabilities CAPABILITY_IAM \
		--parameter-overrides \
			AcmCertificateArn=$(ACM_CERTIFICATE_ARN) \
			SiteId=$(SITE_ID) \
			DomainName=$(DOMAIN_NAME)
