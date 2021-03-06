from dumper.pollution_dumper import PollutionDumper
from dumper.fs_adapter.adapter import FileSystemAdapter


class OZDumper(PollutionDumper):
    def __init__(self, http_host: str, api_key: str, output_path: str, fs_adapter: FileSystemAdapter):
        PollutionDumper.__init__(self, http_host, api_key, output_path, fs_adapter)

    def to_address(self, latitude, longitude, time):
        return "{}/o3/{},{}/{}.json?appid={}".format(self._http_host, latitude, longitude, time, self._api_key)
