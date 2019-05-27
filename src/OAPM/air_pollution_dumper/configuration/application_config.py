from air_pollution_dumper.configuration.api_config import APIConfig
from air_pollution_dumper.configuration.fs_config import FSConfig
from air_pollution_dumper.configuration.kafka_producer_config import KafkaProducerConfig


class ApplicationConfig:
    def __init__(self, api_config: APIConfig, fs_config: FSConfig, kafka_config: KafkaProducerConfig,
                 additional_configs: dict):
        self.__api_config = api_config
        self.__fs_config = fs_config
        self.__kafka_config = kafka_config
        self.__additional_configs = additional_configs

    def get_api_config(self) -> APIConfig:
        return self.__api_config

    def get_fs_config(self) -> FSConfig:
        return self.__fs_config

    def get_kafka_config(self) -> KafkaProducerConfig:
        return self.__kafka_config

    def get_additional_configs(self) -> dict:
        return self.__additional_configs

    def __eq__(self, other):
        return isinstance(other, ApplicationConfig) \
               and other.__api_config == self.__api_config \
               and other.__fs_config == self.__fs_config \
               and other.__kafka_config == self.__kafka_config

    def __str__(self):
        return """
        [API]
        {}
        [FS]
        {}
        [KAFKA]
        {}""".format(self.get_api_config(), self.get_fs_config(), self.get_kafka_config())

    def __repr__(self):
        return str(self)

    @staticmethod
    def parse_from_file(path):
        file = open(path, "r+t")
        configs = {}

        current = None
        for line in file:
            if "[" in line and "]" in line:
                header = line.split("[")[1].split("]")[0]
                configs[header] = []
                current = configs[header]
            if current is not None:
                current.append(line)
        file.close()
        return ApplicationConfig(APIConfig.parse_from_lines(configs["WEATHER_MAP_CONFIG"]),
                                 FSConfig.parse_from_lines(configs["FS_CONFIG"]),
                                 KafkaProducerConfig.parse_from_lines(configs["KAFKA_CONFIG"]),
                                 prepare_configs(configs))


def prepare_configs(configs: dict):
    ret_dict = {}
    for k, v in configs.items():
        temp = filter(lambda i: ":" in i, v)
        temp = [line.split(":", 1) for line in temp]
        values = {prepare(x[0]).upper(): prepare(x[1]) for x in temp}
        ret_dict[k] = values
    return ret_dict


def prepare(line):
    temp = line
    while temp[0] in " \t\n":
        temp = temp[1:]
    while temp[-1] in " \t\n":
        temp = temp[:-1]
    return temp
