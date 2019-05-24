from abc import abstractmethod

import requests

from dumper.fs_adapter.adapter import FileSystemAdapter


class PollutionDumper:
    def __init__(self, http_host: str, api_key: str, output_path: str, fs_adapter: FileSystemAdapter, logger):
        self._http_host = http_host
        self._api_key = api_key
        self._output_path = output_path
        self._fs_adapter = fs_adapter
        self._logger = logger

    def dump(self, latitude, longitude, time):
        path = FileSystemAdapter.to_file_path(self._output_path, latitude, longitude, time)
        self._logger.info("Trying find in file system")
        if self._fs_adapter.is_exist(path):
            self._logger.info("Was founded in file system")
            return self._fs_adapter.read_file(path)
        self._logger.info("Trying to fetch from server")
        response = requests.get(self.to_address(latitude, longitude, time))
        if response.status_code != 200:
            self._logger.info("Can't find records on server")
            raise ConnectionError("Can't find records")
        content = str(response.content)
        self._logger.info("Records was founded")
        self._fs_adapter.mkdir(self._output_path)
        self._logger.info("Dumping records")
        self._fs_adapter.write_file(path, content)
        return content

    @abstractmethod
    def to_address(self, latitude, longitude, time):
        raise NotImplementedError("This functionality is not implemented")
