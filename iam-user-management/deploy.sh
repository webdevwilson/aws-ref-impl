#!/bin/bash

# Requires env variables S3_BUCKET and FROM_EMAIL_ADDRESS

STACK_NAME=$(basename $(pwd))

aws cloudformation package \
  --template-file template.yml \
  --s3-bucket "${S3_BUCKET}" \
  --output-template-file template.pkg.yml

aws cloudformation deploy \
  --template-file template.pkg.yml \
  --stack-name "${STACK_NAME}" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    "FromEmailAddress=${FROM_EMAIL_ADDRESS}"
