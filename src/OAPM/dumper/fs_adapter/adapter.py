from abc import abstractmethod


class FileSystemAdapter:

    @abstractmethod
    def write_file(self, path: str, data):
        raise NotImplementedError("Writing is not implemented")

    @abstractmethod
    def append_to_file(self, path: str, data):
        raise NotImplementedError("Appending is not implemented")

    @abstractmethod
    def read_file(self, path: str):
        raise NotImplementedError("Reading is not implemented")

    @abstractmethod
    def remove_file(self, path: str):
        raise NotImplementedError("Removing is not implemented")

    @abstractmethod
    def mkdir(self, path: str):
        raise NotImplementedError("Mkdir is not implemented")

    @abstractmethod
    def ls(self, path: str):
        raise NotImplementedError("Ls is not implemented")

    def is_exist(self, path: str):
        raise NotImplementedError("Exist is not implemented")

    def to_file_path(self, dir: str, latitude, longitude, year):
        return "{}/t{}_l{}_y{}.json".format(str(dir), str(latitude), str(longitude), str(year))
