package com.cascade.openap.conf

class KafkaConsumerConfig(servers: String,
                          clientId: String,
                          groupId: String,
                          keyDeserializer: String,
                          valueDeserializer: String,
                          autoOffsetReset: String,
                          enableAutoCommit: Boolean,
                          autoCommitIntervalMs: Int,
                          sessionTimeoutMs: Int,
                          securityProtocol: String) {

}

object KafkaConsumerConfig {
  def apply(servers: String,
            clientId: String,
            groupId: String,
            keyDeserializer: String,
            valueDeserializer: String,
            autoOffsetReset: String,
            enableAutoCommit: Boolean,
            autoCommitIntervalMs: Int,
            sessionTimeoutMs: Int,
            securityProtocol: String): KafkaConsumerConfig = new KafkaConsumerConfig(servers, clientId, groupId, keyDeserializer, valueDeserializer, autoOffsetReset, enableAutoCommit, autoCommitIntervalMs, sessionTimeoutMs, securityProtocol)

  def parseFormLines(lines: Seq[String]): KafkaConsumerConfig = {
    val temp = lines.filter(_.contains(":"))

    val splited = temp.map(_.split(":", 1))
    val values = splited.map(x => (prepare(x(0).toUpperCase()), prepare(x(1)))).toMap

    new KafkaConsumerConfig(
      values("SERVERS"),
      values("CLIENT_ID"),
      values("GROUP_ID"),
      values.getOrElse("KEY_DESERIALIZER", "org.apache.kafka.common.serialization.StringDeserializer"),
      values.getOrElse("VALUE_DESERIALIZER", "org.apache.kafka.common.serialization.StringDeserializer"),
      values.getOrElse("AUTO_OFFSET_RESET", "0"),
      values.getOrElse("ENABLE_AUTO_COMMIT", "False").toBoolean,
      values.getOrElse("AUTO_COMMIT_INTERVAL_MS", "1").toInt,
      values.getOrElse("SESSION_TIMEOUT_MS", "30000").toInt,
      values.getOrElse("SECURITY_PROTOCOL", "PLAINTEXT"))
  }

  def prepare(strLine: String): String = {
    var line = strLine
    if (line.startsWith(" ") || line.startsWith("\t") || line.startsWith("\n")) {
      line = line.substring(1)
    }
    else if (line.endsWith(" ") || line.endsWith("\t") || line.endsWith("\n")) {
      line = line.substring(0, line.length - 1)
    }
    line
  }

}