package com.cascade.openap.conf

class AppConfig (val consumerGroupId: String,
                 val consumerBootstrapServers: String,
                 val consumerAutoOffsetReset: String,
                 val sparkMaster: String,
                 val streamTime: Long,
                 val coInputTopic: String,
                 val noInputTopic: String,
                 val ozInputTopic: String,
                 val soInputTopic: String
) {
}
object AppConfig {
  def readAppConfig(path: Array[String]): AppConfig = {

    new AppConfig(
      "consumer_id",
      "localhost:9092",
      "earliest",
      "local[*]",
      5,
      "co-topic",
      "no-topic",
      "oz-topic",
      "so-topic"
    )
  }
}
