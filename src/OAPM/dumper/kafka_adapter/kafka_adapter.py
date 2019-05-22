from kafka import KafkaProducer

from configuration.kafka_producer_config import KafkaProducerConfig


class KafkaSender:
    def __str__(self):
        """
        used for logging added handlers to stream
        :return: name of handler
        """
        return "Kafka producer handler"

    def __init__(self, kafka_config: KafkaProducerConfig):
        """
        :param kafka_config: kafka config
        """

        self._kafka_config = kafka_config
        self._producer = KafkaProducer(bootstrap_servers=kafka_config.get_servers(),
                                       client_id=kafka_config.get_client_id(),
                                       value_serializer=kafka_config.get_value_serializer(),
                                       key_serializer=kafka_config.get_key_serializer(),
                                       acks=kafka_config.get_acks(),
                                       compression_type=kafka_config.get_compression_type(),
                                       retries=kafka_config.get_retries(),
                                       batch_size=kafka_config.get_batch_size(),
                                       max_request_size=kafka_config.get_max_request_size(),
                                       request_timeout_ms=kafka_config.get_request_timeout_ms(),
                                       security_protocol=kafka_config.get_security_protocol(),
                                       api_version=(0, 10, 1))

    def send_message(self, topic, message, key):
        print(topic, message, key)
        self._producer.send(topic, message, key).add_callback(print("succesfull")).get(timeout=30)
        self._producer.flush()
