class APIConfig:

    def __init__(self, api_key: str, host: str):
        self.__api_key = api_key
        self.__host = host

    def get_api_key(self) -> str:
        return self.__api_key

    def get_host(self) -> str:
        return self.__host

    def __eq__(self, other):
        return isinstance(other, APIConfig) \
               and other.__api_key == self.__api_key \
               and other.__host == self.__host

    def __str__(self):
        return "API: {}, HOST: {}".format(self.get_api_key(), self.get_host())

    def __repr__(self):
        return str(self)

    @staticmethod
    def parse_from_lines(lines):
        temp = filter(lambda i: ":" in i, lines)
        temp = [line.split(":", 1) for line in temp]
        values = {prepare(x[0]).upper(): prepare(x[1]) for x in temp}
        return APIConfig(values["API_KEY"], values["API_HOST"])


def prepare(line):
    temp = line
    while temp[0] in " \t\n":
        temp = temp[1:]
    while temp[-1] in " \t\n":
        temp = temp[:-1]
    return temp
