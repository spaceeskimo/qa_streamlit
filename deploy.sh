#!/usr/bin/env bash

IMAGE_NAME=$1
### ECR - build images and push to remote repository

echo "Building image: $IMAGE_NAME:latest"

docker build --rm -t $IMAGE_NAME:latest .

eval $(aws ecr get-login --no-include-email)

docker tag $IMAGE_NAME 177085113002.dkr.ecr.eu-central-1.amazonaws.com/$IMAGE_NAME:latest
docker push 177085113002.dkr.ecr.eu-central-1.amazonaws.com/$IMAGE_NAME:latest

aws ecs update-service --force-new-deployment --cluster $IMAGE_NAME --service $IMAGE_NAME-web-server
