import dumper.configuration.api_config as api
import dumper.configuration.fs_config as fs
import dumper.configuration.kafka_producer_config as kafka


class ApplicationConfig:
    def __init__(self, api_config, fs_config, kafka_config):
        self.__api_config = api_config
        self.__fs_config = fs_config
        self.__kafka_config = kafka_config

    def get_api_config(self):
        return self.__api_config

    def get_fs_config(self):
        return self.__fs_config

    def get_kafka_config(self):
        return self.__kafka_config


def parse_from_file(path):
    file = open(path, "r+t")
    api_list = []
    fs_list = []
    kafka_list = []

    current = None
    for line in file:
        if "WEATHER_MAP_CONFIG" in line:
            current = api_list
        elif "FS_CONFIG" in line:
            current = fs_list
        elif "KAFKA_CONFIG" in line:
            current = kafka_list
        if current is not None:
            current.append(line)
    file.close()
    return ApplicationConfig(api.parse_from_lines(api_list),
                             fs.parse_from_lines(fs_list),
                             kafka.parse_from_lines(kafka_list))
