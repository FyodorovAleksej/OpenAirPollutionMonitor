from abc import abstractmethod

import requests

from dumper.fs_adapter.adapter import FileSystemAdapter
import json

class PollutionDumper:
    def __init__(self, http_host: str, api_key: str, output_path: str, fs_adapter: FileSystemAdapter):
        self._http_host = http_host
        self._api_key = api_key
        self._output_path = output_path
        self._fs_adapter = fs_adapter

    def dump(self, latitude, longitude, time):
        response = requests.get(self.to_address(latitude, longitude, time))
        if response.status_code != 200:
            raise ConnectionError("Can't find records")
        return str(response.content)

    @abstractmethod
    def to_address(self, latitude, longitude, time):
        raise NotImplementedError("This functionality is not implemented")
