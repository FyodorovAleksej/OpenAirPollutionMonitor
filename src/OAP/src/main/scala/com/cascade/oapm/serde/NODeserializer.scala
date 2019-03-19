package com.cascade.oapm.serde

import java.util

import org.apache.kafka.common.serialization.Deserializer

class NODeserializer[T] extends Deserializer[T] {

  override def configure(conf: util.Map[String, _], isKey: Boolean): Unit = {
    
  }

  override def deserialize(topic: String, message: Array[Byte]): T = {
    val mes = new String(message)
    mes.asInstanceOf[T]
  }

  override def close(): Unit = {

  }
}
