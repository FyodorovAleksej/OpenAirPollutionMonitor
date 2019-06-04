#!/usr/bin/env bash

set -ex

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

cd /

SPARK_MAJOR_VERSION=2
sleep 20

${SPARK_HOME}/bin/spark-submit \
  --class com.cascade.openap.SparkApp \
  --master "${SPARK_MASTER:-local[*]}" \
  --conf spark.executor.instances=2 \
  --conf spark.driver.memory=1024M \
  --conf spark.executor.memory=1024M \
  ${APP_JAR}