package com.cascade.oapm

import com.cascade.oapm.conf.{ApplicationConfig, ConfigParser}
import org.apache.avro.AvroRuntimeException
import org.apache.kafka.clients.consumer.{ConsumerConfig, ConsumerRecord}
import org.apache.kafka.clients.producer.ProducerConfig
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.streaming.kafka010.ConsumerStrategies.Subscribe
import org.apache.spark.streaming.kafka010.LocationStrategies.PreferConsistent
import org.apache.spark.streaming.kafka010._
import org.slf4j.LoggerFactory
import org.xml.sax.SAXParseException

object OapApplication {
    private val LOGGER = LoggerFactory.getLogger(OapApplication.getClass)

    def main(args: Array[String]) {
      val props = ConfigParser.parseConfig("./src/main/resources/config/application.properties")

      val appConfig = ApplicationConfig(props)

      val consumerParams = Map[String, Object](
        ProducerConfig.BOOTSTRAP_SERVERS_CONFIG -> appConfig.bootstrapServes,
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
      sconf.setAppName("Open Air Pollution Streaming Spark App")

      val streamingContext = new StreamingContext(sconf, Seconds(appConfig.streamTime))


      val stream = KafkaUtils.createDirectStream[String, String](
        streamingContext,
        PreferConsistent,
        Subscribe[String, String](Array(appConfig.coTopic, appConfig.soTopic, appConfig.noTopic), consumerParams)
      )

      stream.foreachRDD { rdd =>
        val sender = new KafkaSender(appConfig)

        val offsetRanges = rdd.asInstanceOf[HasOffsetRanges].offsetRanges

        rdd.foreach { xmlPair: ConsumerRecord[String, String] =>
          try {
            // AvroSchema object is not serializable, somehow pass otherwise
            val shortSchema = xmlConvertor.readSchema(appConfig.outputSchema)
            val fullMessage = xmlConvertor.convertToAvro(xmlPair.value)
            val shortMessage = Conversion.extractSubschema(fullMessage, shortSchema)

            val serializer = AvroSerializerType.createSerializer(appConfig.outputFormat, shortMessage)
            val shortAvroBytes = serializer.write()
            sender.send(shortAvroBytes, appConfig.outputTopic)
          }
          catch {
            case _: SAXParseException | _: AvroRuntimeException => {
              System.out.println("Failed to convert XML message") // TODO add more details: topic name, msg offset AND EXCEPTION
              sender.send(xmlPair.value().getBytes(), appConfig.errorTopic)
            }
          }

        }
        sender.close()
        stream.asInstanceOf[CanCommitOffsets].commitAsync(offsetRanges)
      }

      streamingContext.start()
      streamingContext.awaitTermination()
      LOGGER.error("Streaming batch finished")
    }

  }


