package com.cascade.openap

import com.cascade.openap.conf.AppConfig
import org.apache.kafka.clients.consumer.ConsumerConfig
import org.apache.kafka.clients.producer.ProducerConfig
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark._
import org.apache.spark.sql.SparkSession
import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka010.ConsumerStrategies.Subscribe
import org.apache.spark.streaming.kafka010.LocationStrategies.PreferConsistent
import org.apache.spark.streaming.kafka010._
import org.slf4j.LoggerFactory


/**
  * Spark Streaming app that reads Kafka topic messages as XML and
  * writes the data converted in AVRO format into another topic.
  */
object SparkApp {
  private val LOGGER = LoggerFactory.getLogger(SparkApp.getClass)

  def main(args: Array[String]) {
    val appConfig = AppConfig.readAppConfig(args)

    val consumerParams = Map[String, Object](
      ProducerConfig.BOOTSTRAP_SERVERS_CONFIG -> appConfig.consumerBootstrapServers,
      ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG -> classOf[StringDeserializer],
      ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG -> classOf[StringDeserializer],
      ConsumerConfig.GROUP_ID_CONFIG -> appConfig.consumerGroupId,
      ConsumerConfig.AUTO_OFFSET_RESET_CONFIG -> appConfig.consumerAutoOffsetReset,
      ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG -> java.lang.Boolean.FALSE
    )

    val sconf: SparkConf = new SparkConf()
    if (appConfig.sparkMaster != null) {
      sconf.setMaster(appConfig.sparkMaster)
    }
    sconf.setAppName("OAP_streaming_app")
    sconf.set("spark.testing.memory", "2147480000")


    val spark: SparkSession = SparkSession.builder().config(sconf).getOrCreate()
    val sc = spark.sparkContext // Just used to create test RDDs

    val streamingContext = new StreamingContext(sc, Seconds(appConfig.streamTime))

    val stream = KafkaUtils.createDirectStream[String, String](
      streamingContext,
      PreferConsistent,
      Subscribe[String, String](Array(appConfig.coInputTopic,
        appConfig.noInputTopic,
        appConfig.ozInputTopic,
        appConfig.soInputTopic), consumerParams)
    )

    val basePath = "/shared/"
    val format = "csv"
    val saveMode = "append"
    val storePrefix = "oap_out"

    stream.foreachRDD(
      rdd => {
        val mapped = rdd.map(x => parseRecord(x.key(), x.value(), x.topic()))
        val df = spark.createDataFrame(mapped).toDF("topic", "latitude", "longitude", "year", "value")
        df.show()
        df.write
          .partitionBy("topic")
          .format(format)
          .mode(saveMode)
          .save(basePath + storePrefix + "/")
      })


    streamingContext.start()
    streamingContext.awaitTermination()
    LOGGER.error("Streaming batch finished")
  }

  def parseRecord(key: String, value: String, topic: String): PollutionRecord = {
    val latitudeIndex = key.indexOf("t") + 1
    val longitudeIndex = key.indexOf("l") + 1
    val yearIndex = key.indexOf("y") + 1

    val latitude = key.substring(latitudeIndex).split("_")(0)
    val longitude = key.substring(longitudeIndex).split("_")(0)
    val year = key.substring(yearIndex).split("\\.")(0)

    PollutionRecord(topic, latitude.toLong, longitude.toLong, year.toLong, value.toDouble)
  }

  case class PollutionRecord(topic: String,
                             latitude: Long,
                             longitude: Long,
                             year: Long,
                             value: Double)

}