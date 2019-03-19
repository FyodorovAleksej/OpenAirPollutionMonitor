package com.cascade.oapm.conf
import java.util

class ApplicationConfig(
                       // KAFKA
                       val bootstrapServes: String,
                       val consumerGroupId: String,
                       val consumerAutoOffsetReset: String,

                       val soTopic: String,
                       val noTopic: String,
                       val coTopic: String,

                       // SPARK
                       val sparkMaster: String,
                       val streamTime: String) {
}
object ApplicationConfig {
  def apply(conf: util.Map[String, String]): ApplicationConfig =
    new ApplicationConfig(
      // KAFKA
      bootstrapServes = conf.get("consumer.bootstrap.servers"),
      consumerGroupId = conf.get("consumer.group.id"),
      consumerAutoOffsetReset = conf.get("consumer.reset.offset"),
      soTopic = conf.get("consumer.sotopic"),
      noTopic = conf.get("consumer.notopic"),
      coTopic = conf.get("consumer.cotopic"),
      // SPARK
      sparkMaster = conf.get("spark.master"),
      streamTime = conf.get("spark.stream.time"))
}
