#!/bin/bash 
# Copyright 2022 Balacoon

docker run -it --rm -v $PWD:/home --user $(id -u):$(id -g) learn_to_pronounce:latest /bin/bash
