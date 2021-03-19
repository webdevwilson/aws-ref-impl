SAM_PKG_TEMPLATE := dist/template.pkg.yml
SAM_STACK_NAME := sam-api
SAM_TEMPLATE := template.yml

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
		--capabilities CAPABILITY_IAM