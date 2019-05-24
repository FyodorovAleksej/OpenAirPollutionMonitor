import logging
import os

from dumper.configuration.fs_config import FSConfig
from dumper.fs_adapter.adapter import FileSystemAdapter


class DefaultFileSystem(FileSystemAdapter):
    logger = logging.getLogger("dumper.fs_adapter.DefaultFileSystem")

    def __init__(self, config: FSConfig):
        self.__config = config

    def write_file(self, path: str, data):
        DefaultFileSystem.logger.info("Write to file = {}".format(self.sum_path(path)))
        file = open(self.sum_path(path), "w")
        file.write(data)
        file.flush()
        file.close()

    def append_to_file(self, path: str, data):
        DefaultFileSystem.logger.info("Append to file = {}".format(self.sum_path(path)))
        file = open(self.sum_path(path), "a")
        file.write(data)
        file.flush()
        file.close()

    def remove_file(self, path: str):
        DefaultFileSystem.logger.info("Remove file = {}".format(self.sum_path(path)))
        os.remove(self.sum_path(path))

    def mkdir(self, path):
        DefaultFileSystem.logger.info("Makedir for path = {}".format(self.sum_path(path)))
        if not os.path.exists(self.sum_path(path)):
            os.mkdir(self.sum_path(path))

    def ls(self, path):
        return os.listdir(self.sum_path(path))

    def read_file(self, path):
        DefaultFileSystem.logger.info("Read file = {}".format(self.sum_path(path)))
        file = open(self.sum_path(path), "r")
        text = file.read()
        file.close()
        return text

    def is_exist(self, path: str):
        return os.path.exists(self.sum_path(path))

    def sum_path(self, path):
        return self.__config.get_dir() + path
