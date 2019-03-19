package com.cascade.oapm.serde

import java.util

import org.apache.kafka.common.serialization.Deserializer

class DeserializerBuilder(noTopic: String,
                          coTopic: String,
                          soTopic: String,
                          config: util.Map[String, _]) {

  def buildDeserializerForTopic[T](topic: String): Deserializer[T] = {
    topic match {
      case x if x.equalsIgnoreCase(noTopic) => buildForNo[T]()
      case x if x.equalsIgnoreCase(coTopic) => buildForCo[T]()
      case x if x.equalsIgnoreCase(soTopic) => buildForSo[T]()
      case _ => throw new NotImplementedError("deserializer for this topic isn't supported")
    }
  }

  private def buildForNo[T](): NODeserializer[T] = {
    val deserializer = new NODeserializer[T]
    deserializer.configure(config, isKey = false)
    deserializer
  }

  private def buildForSo[T](): NODeserializer[T] = {
    val deserializer = new SODeserializer[T]
    deserializer.configure(config, isKey = false)
    deserializer
  }

  private def buildForCo[T](): NODeserializer[T] = {
    val deserializer = new CODeserializer[T]
    deserializer.configure(config, isKey = false)
    deserializer
  }
}
