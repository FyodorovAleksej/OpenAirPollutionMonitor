from json import dumps
from time import sleep

from kafka import KafkaProducer


def serializer(x):
    dumps(x).encode('utf-8')


class KafkaSender:
    def __init__(self, bootstrap_servers, value_serializer=serializer):
        self.__bootstrap_servers = bootstrap_servers
        self.__value_serializer = value_serializer
        self.__producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=value_serializer)

    def send(self, topic, data, key):
        self.__producer.send(topic, data, key)
