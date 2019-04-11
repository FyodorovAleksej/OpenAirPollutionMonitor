from kafka import KafkaProducer


class KafkaSender:
    def __str__(self):
        """
        used for logging added handlers to stream
        :return: name of handler
        """
        return "Kafka producer handler"

    def __init__(self, servers):
        """
        :param servers: list of kafka bootstrap servers
        """
        self._producer = KafkaProducer(bootstrap_servers=servers,
                                       value_serializer=lambda v: v.encode('utf-8'),
                                       key_serializer=lambda k: k.encode('utf-8'),
                                       client_id="kafka_dumper",
                                       api_version=(0, 10, 1))

    def send_message(self, topic, message, key):
        print(topic, message, key)
        self._producer.send(topic, message, key).get(timeout=30)
