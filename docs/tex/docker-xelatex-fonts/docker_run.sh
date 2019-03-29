#!/bin/bash

IMAGE=tex:1
NAME=ctex
HOST_FOLDER="$(pwd)/doc"
CONTAINER_FOLDER="/doc"

docker stop $NAME
docker rm $NAME

docker build -t $IMAGE .
docker run -d -it --name $NAME -v $HOST_FOLDER:$CONTAINER_FOLDER -w $CONTAINER_FOLDER $IMAGE
