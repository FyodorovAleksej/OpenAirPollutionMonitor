class APIConfig:

    def __init__(self, api_key, host):
        self.__api_key = api_key
        self.__host = host

    def get_api_key(self):
        return self.__api_key

    def get_host(self):
        return self.__host


def parse_from_lines(lines):
    temp = filter(lambda i: ":" in i, lines)
    temp = [line.split(":", 2) for line in temp]
    values = {prepare(x[0]).upper(): prepare(x[1]) for x in temp}
    return APIConfig(values["API_KEY"], values["API_HOST"])


def prepare(line):
    temp = line
    while temp[0] in " \t\n":
        temp = temp[1:]
    while temp[-1] in " \t\n":
        temp = temp[:-1]
    return temp
