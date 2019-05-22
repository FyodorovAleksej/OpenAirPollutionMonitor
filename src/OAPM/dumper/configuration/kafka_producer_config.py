class KafkaProducerConfig:
    def __init__(self, servers,
                 client_id,
                 key_serializer,
                 value_serializer,
                 acks,
                 compression_type,
                 retries,
                 batch_size,
                 max_request_size,
                 request_timeout_ms,
                 security_protocol):
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

    def get_servers(self):
        return self.__servers

    def get_client_id(self):
        return self.__client_id

    def get_key_serializer(self):
        return self.__key_serializer

    def get_value_serializer(self):
        return self.__value_serializer

    def get_acks(self):
        return self.__acks

    def get_compression_type(self):
        return self.__compression_type

    def get_retries(self):
        return self.__retries

    def get_batch_size(self):
        return self.__batch_size

    def get_max_request_size(self):
        return self.__max_request_size

    def get_request_timeout_ms(self):
        return self.__request_timeout_ms

    def get_security_protocol(self):
        return self.__security_protocol


def parse_from_lines(lines):
    temp = filter(lambda i: ":" in i, lines)
    temp = [line.split(":", 2) for line in temp]
    values = {prepare(x[0]).upper(): prepare(x[1]) for x in temp}
    return KafkaProducerConfig(values.get("SERVERS"),
                               values.get("CLIENT_ID"),
                               values.get("KEY_SERIALIZER", lambda v: v.encode("utf-8")),
                               values.get("VALUE_SERIALIZER", lambda v: v.encode("utf-8")),
                               values.get("ACKS", 1),
                               values.get("COMPRESSION_TYPE", None),
                               values.get("RETRIES", 0),
                               values.get("BATCH_SIZE", 16384),
                               values.get("MAX_REQUEST_SIZE", 1048576),
                               values.get("REQUEST_TIMEOUT_MS", 30000),
                               values.get("SECURITY_PROTOCOL", "PLAINTEXT"))


def prepare(line):
    temp = line
    while temp[0] in " \t\n":
        temp = temp[1:]
    while temp[-1] in " \t\n":
        temp = temp[:-1]
    return temp
