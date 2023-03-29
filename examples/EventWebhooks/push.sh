#!/bin/bash
echo "See https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry"
echo "Please login using"
echo "export CR_PAT=YOUR_TOKEN"
echo "echo \$CR_PAT | docker login ghcr.io -u USERNAME --password-stdin"
echo "before calling this script"
$(dirname $0)/build.sh --platform linux/arm64/v8 --platform linux/amd64 --push

