FROM apache/zeppelin:0.8.1

RUN wget http://apache.mirror.triple-it.nl/spark/spark-2.3.3/spark-2.3.3-bin-hadoop2.7.tgz \
&&  tar -xzf spark-2.3.3-bin-hadoop2.7.tgz \
&&  mv spark-2.3.3-bin-hadoop2.7 /opt/spark

ENV SPARK_HOME=/opt/spark
ENV PYTHONPATH=/opt/spark/python;/opt/spark/python/lib/py4j-*-src.zip
ENV SPARK_MAJOR_VERSION=2
ENV spark.app.name=Zeppelin_Spark2
ENV zeppelin.spark.enableSupportedVersionCheck=false

