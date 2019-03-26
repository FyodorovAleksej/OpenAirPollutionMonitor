package com.cascade.openap
import java.util.Properties
import java.util.concurrent.TimeUnit

import org.apache.kafka.clients.producer.{KafkaProducer, ProducerConfig, ProducerRecord}
import org.apache.kafka.common.serialization.StringSerializer
object Producer {
  def main(args: Array[String]): Unit = {
    val conf = new java.util.HashMap[String, AnyRef]()
    conf.put("bootstrap.servers", "kafka:6667")
    conf.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer")
    conf.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer")

  val producer = new KafkaProducer[String, String](conf)
    producer.send(new ProducerRecord[String, String]("co-topic", "test_message"))
    producer.close(100L, TimeUnit.MILLISECONDS)
  }
}
