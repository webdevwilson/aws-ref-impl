# docker-awscli-ecr

Used to build a docker image that contains the tools necessary to build docker images and push
to ECR

## Push to ECR

```
REGION=<region>
REPO=<name of repo>
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPO_URL=${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO}

docker build -t ${REPO_URL}:latest .

# Docker Login to ECR
eval $(aws ecr get-login --region ${REGION} --no-include-email)
# - or -
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${REPO_URL}

docker push ${REPO_URL}:latest
```