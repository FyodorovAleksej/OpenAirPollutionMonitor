FROM openjdk:8-jdk-alpine

MAINTAINER fyodorovas

RUN apk update \
      && apk upgrade \
      && apk add --update bash \
      && apk add --update curl \
      && rm -rf /var/cache/apk/*

ENV INSTALL_DIR /usr/local
ENV SPARK_HOME $INSTALL_DIR/spark

ENV SPARK_VERSION 2.3.3
ENV HADOOP_VERSION 2.7
ENV SPARK_TGZ_URL https://www.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz

ENV APP_TAR_GZ oap-spark-*.tar.gz
ENV APP_JAR oap-spark-*.jar

WORKDIR $INSTALL_DIR

RUN set -x \
      && curl -fSL "$SPARK_TGZ_URL" -o spark.tgz \
      && tar -xzf spark.tgz \
      && mv spark-* spark \
      && rm spark.tgz \
      && mkdir -p /input/

COPY scripts/*.sh /

RUN chmod +x /*.sh

WORKDIR /

COPY build/distributions/$APP_TAR_GZ /
RUN tar xvf $APP_TAR_GZ

ENTRYPOINT ["/startDocker.sh"]