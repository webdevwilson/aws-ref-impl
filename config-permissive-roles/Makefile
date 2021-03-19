PKG = template.pkg.yaml
CFN_STACK = config-permissive-roles
IAM_REFERENCE = iam_reference.json

clean:
	rm -f $(PKG)
	rm -f $(IAM_REFERENCE)

$(PKG):
	aws cloudformation package \
	 	--template-file template.yaml \
	 	--output-template-file $(PKG) \
		--s3-bucket $(CODE_BUCKET)

deploy: $(PKG)
	aws cloudformation deploy \
		--template-file $(PKG) \
		--stack-name $(CFN_STACK) \
		--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM

$(IAM_REFERENCE):
	git submodule update --init
	python3 src/update_iam_reference.py iam-reference/services/ > $(IAM_REFERENCE)

test:
	python3 src/policies_test.py -k test_unit

integration-test:
	aws cloudformation deploy \
		--template-file src/it_fixtures.yaml \
		--stack-name test-config-permissive-roles \
		--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM
	python3 src/policies_test.py -k test_int
	# aws cloudformation delete-stack \
	# 	--stack-name test-config-permissive-roles


.PHONY = clean deploy test integration-test