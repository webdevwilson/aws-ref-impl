aws cloudformation deploy \
  --template-file template.yml \
  --stack-name codebuild-npm-codeartifacts \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1