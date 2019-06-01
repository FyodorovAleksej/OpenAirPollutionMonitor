#!/usr/bin/env bash

set -ex

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

${SPARK_HOME}/bin/spark-class org.apache.spark.deploy.master.Master \
    --ip ${SPARK_LOCAL_IP} \
    --port ${SPARK_MASTER_PORT} \
    --webui-port ${SPARK_MASTER_WEBUI_PORT}