#!/usr/bin/env bash

docker pull gradle:jdk8
docker run --rm -u root -v $(pwd):/home/gradle/project -w /home/gradle/project gradle:jdk8 gradle clean jar tar
