#!/bin/bash
pushd $(dirname $0)
repo=ghcr.io
namespace=trellis-logic
image_name=event-webhooks
tag=1.0
buildargs="--build-arg basedir=EventWebhooks/"
if [[ "$@" != *"--push"* ]]; then
    buildargs="$buildargs --output=type=docker"
fi
docker buildx build ${buildargs} -f Dockerfile -t ${repo}/${namespace}/${image_name}:${tag} $@ ..
