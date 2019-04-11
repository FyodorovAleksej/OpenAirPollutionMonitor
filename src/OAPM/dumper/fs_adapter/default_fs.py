import os

from dumper.fs_adapter.adapter import FileSystemAdapter


class DefaultFileSystem(FileSystemAdapter):
    def write_file(self, path: str, data):
        file = open(path, "w")
        file.write(data)
        file.flush()
        file.close()

    def append_to_file(self, path: str, data):
        file = open(path, "a")
        file.write(data)
        file.flush()
        file.close()

    def remove_file(self, path: str):
        os.remove(path)

    def mkdir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def ls(self, path):
        return os.listdir(path)

    def read_file(self, path):
        file = open(path, "r")
        text = file.read()
        file.close()
        return text

    def is_exist(self, path: str):
        return os.path.exists(path)
