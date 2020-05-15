ACCOUNT_ID := $(shell aws sts get-caller-identity --query Account --output text)
REPO_URL := $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/$(REPO)

build:
	docker build -t $(REPO_URL):latest .

login:
	@echo $(aws ecr get-login --region $(REGION) --no-include-email))

push: build login
	docker push $(REPO_URL):latest

.PHONY: build login push