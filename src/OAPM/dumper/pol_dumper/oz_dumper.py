import logging

from dumper.pol_dumper.pollution_dumper import PollutionDumper
from dumper.fs_adapter.adapter import FileSystemAdapter


class OZDumper(PollutionDumper):
    logger = logging.getLogger("dumper.OZDumper")

    def __init__(self, http_host: str, api_key: str, output_path: str, fs_adapter: FileSystemAdapter):
        PollutionDumper.__init__(self, http_host, api_key, output_path, fs_adapter, OZDumper.logger)

    def to_address(self, latitude, longitude, time):
        return "{}/o3/{},{}/{}.json?appid={}".format(self._http_host, latitude, longitude, time, self._api_key)
