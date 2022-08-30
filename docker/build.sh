#!/bin/bash 
# Copyright 2022 Balacoon

set -e
set -x

usage() {
    cat <<EOF
Usage:
bash $1 [--tag some_tag] [--build-pg] [--no-cache]

Arguments:
tag - tag of docker image, by default "latest"
build-pg - balacoon_pronunciation_generation package is built from sources (private package)
no-cache - rebuild all docker layers from scratch
EOF
}

docker_image_name="learn_to_pronounce"
tag="latest"
build_pg_opt=""
no_cache_opt=""
ssh_keys_opt=""
while [ "$1" != "" ]; do
    case $1 in
        --tag )
            shift
            tag=$1
        ;;
        --build-pg )
            build_pg_opt="--build-arg build_pg=true"
        ;;
        --no-cache )
	    no_cache_opt="--no-cache"
	;;
        -h | --help ) usage $0
            exit
        ;;
        * ) usage $0
            exit 1
    esac
    shift
done

DOCKER_BUILDKIT=1 docker build --ssh default $no_cache_opt \
	-t $docker_image_name:$tag $build_pg_opt \
	--build-arg user_id=$(id -u) --build-arg group_id=$(id -g) \
	-f docker/Dockerfile .

