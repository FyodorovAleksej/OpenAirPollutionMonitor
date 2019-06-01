package com.cascade.openap

import com.cascade.openap.SparkApp.parseRecord
import com.cascade.openap.conf.SaveConfig
import org.apache.kafka.clients.consumer.ConsumerRecord
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.SparkSession

@SerialVersionUID(20L)
class DataSaver(val config: SaveConfig, spark: SparkSession) extends Serializable {
  def save(rdd: RDD[ConsumerRecord[String, String]]): Unit = {
    val mapped = rdd.map(x => parseRecord(x.key(), x.value(), x.topic()))
    val df = spark.createDataFrame(mapped).toDF("topic", "latitude", "longitude", "year", "value")
    df.show()
    df.write
      .partitionBy("topic")
      .format(config.format)
      .mode(config.mode)
      .save(config.path)
  }
}
