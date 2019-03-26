package com.cascade.openap

import com.cascade.openap.conf.AppConfig
import org.apache.kafka.clients.consumer.{ConsumerConfig, ConsumerRecord}
import org.apache.kafka.clients.producer.ProducerConfig
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark._
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
    sconf.setAppName("XmlToAvro_streaming_app")

    val streamingContext = new StreamingContext(sconf, Seconds(appConfig.streamTime))

    val stream = KafkaUtils.createDirectStream[String, String](
      streamingContext,
      PreferConsistent,
      Subscribe[String, String](Array(appConfig.coInputTopic), consumerParams)
    )

    stream.foreachRDD { rdd =>
      val offsetRanges = rdd.asInstanceOf[HasOffsetRanges].offsetRanges
      rdd.foreach { xmlPair: ConsumerRecord[String, String] =>
        xmlPair.topic()
        println(xmlPair.value())
      }
      println("--COUNT = " + rdd.count())
      stream.asInstanceOf[CanCommitOffsets].commitAsync(offsetRanges)
    }

    streamingContext.start()
    streamingContext.awaitTermination()
    LOGGER.error("Streaming batch finished")
  }
}

