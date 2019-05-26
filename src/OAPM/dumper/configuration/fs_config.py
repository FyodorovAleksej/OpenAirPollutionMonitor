class FSConfig:
    def __init__(self, dir: str, host):
        self.__dir = dir
        self.__host = host

    def get_dir(self) -> str:
        return self.__dir

    def get_host(self) -> str:
        return self.__host

    def __eq__(self, other):
        return isinstance(other, FSConfig) \
               and other.__dir == self.__dir \
               and other.__host == self.__host

    def __str__(self):
        return "DIR: {}, HOST: {}".format(self.get_dir(), self.get_host())

    def __repr__(self):
        return str(self)

    @staticmethod
    def parse_from_lines(lines):
        temp = filter(lambda i: ":" in i, lines)
        temp = [line.split(":", 1) for line in temp]
        values = {prepare(x[0]).upper(): prepare(x[1]) for x in temp}
        return FSConfig(values["DIR"],
                        values.get("HOST", None))


def prepare(line):
    temp = line
    while temp[0] in " \t\n":
        temp = temp[1:]
    while temp[-1] in " \t\n":
        temp = temp[:-1]
    return temp
