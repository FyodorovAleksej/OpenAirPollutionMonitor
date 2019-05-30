class KafkaProducerConfig:
    def __init__(self, servers: str,
                 client_id: str,
                 key_serializer,
                 value_serializer,
                 acks: int,
                 compression_type: str,
                 retries: int,
                 batch_size: int,
                 max_request_size: int,
                 request_timeout_ms: int,
                 security_protocol: str):
        self.__servers = servers
        self.__client_id = client_id
        self.__key_serializer = key_serializer
        self.__value_serializer = value_serializer
        self.__acks = acks
        self.__compression_type = compression_type
        self.__retries = retries
        self.__batch_size = batch_size
        self.__max_request_size = max_request_size
        self.__request_timeout_ms = request_timeout_ms
        self.__security_protocol = security_protocol

    def get_servers(self) -> str:
        return self.__servers

    def get_client_id(self) -> str:
        return self.__client_id

    def get_key_serializer(self):
        return self.__key_serializer

    def get_value_serializer(self):
        return self.__value_serializer

    def get_acks(self) -> int:
        return self.__acks

    def get_compression_type(self) -> str:
        return self.__compression_type

    def get_retries(self) -> int:
        return self.__retries

    def get_batch_size(self) -> int:
        return self.__batch_size

    def get_max_request_size(self) -> int:
        return self.__max_request_size

    def get_request_timeout_ms(self) -> int:
        return self.__request_timeout_ms

    def get_security_protocol(self) -> str:
        return self.__security_protocol

    def __eq__(self, other):
        return isinstance(other, KafkaProducerConfig) \
               and other.__servers == self.__servers \
               and other.__client_id == self.__client_id \
               and other.__acks == self.__acks \
               and other.__compression_type == self.__compression_type \
               and other.__retries == self.__retries \
               and other.__batch_size == self.__batch_size \
               and other.__max_request_size == self.__max_request_size \
               and other.__request_timeout_ms == self.__request_timeout_ms \
               and other.__security_protocol == self.__security_protocol

    def __str__(self):
        return "SERVERS: {}, " \
               "CLIENT_ID: {}, " \
               "KEY_SERIALIZER: {}, " \
               "VALUE_SERIALIZER: {}, " \
               "ACKS: {}, " \
               "COMPRESSION_TYPE: {}, " \
               "RETRIES: {}, " \
               "BATCH_SIZE: {}, " \
               "MAX_REQUEST_SIZE: {}, " \
               "REQUEST_TIMEOUT_MS: {}, " \
               "SECURITY_PROTOCOL: {}" \
            .format(self.get_servers(),
                    self.get_client_id(),
                    self.get_key_serializer(),
                    self.get_value_serializer(),
                    self.get_acks(),
                    self.get_compression_type(),
                    self.get_retries(),
                    self.get_batch_size(),
                    self.get_max_request_size(),
                    self.get_request_timeout_ms(),
                    self.get_security_protocol())

    def __repr__(self):
        return str(self)

    @staticmethod
    def parse_from_lines(lines):
        temp = filter(lambda i: ":" in i, lines)
        temp = [line.split(":", 1) for line in temp]
        values = {prepare(x[0]).upper(): prepare(x[1]) for x in temp}
        return KafkaProducerConfig(values.get("SERVERS"),
                                   values.get("CLIENT_ID"),
                                   values.get("KEY_SERIALIZER", lambda v: v.encode("utf-8")),
                                   values.get("VALUE_SERIALIZER", lambda v: v.encode("utf-8")),
                                   int(values.get("ACKS", 1)),
                                   values.get("COMPRESSION_TYPE", None),
                                   int(values.get("RETRIES", 0)),
                                   int(values.get("BATCH_SIZE", 16384)),
                                   int(values.get("MAX_REQUEST_SIZE", 1048576)),
                                   int(values.get("REQUEST_TIMEOUT_MS", 30000)),
                                   values.get("SECURITY_PROTOCOL", "PLAINTEXT"))


def prepare(line):
    temp = line
    while temp[0] in " \t\n":
        temp = temp[1:]
    while temp[-1] in " \t\n":
        temp = temp[:-1]
    return temp
