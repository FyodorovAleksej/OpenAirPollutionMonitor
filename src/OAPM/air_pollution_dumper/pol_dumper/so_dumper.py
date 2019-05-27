import logging

from air_pollution_dumper.fs_adapter.adapter import FileSystemAdapter
from air_pollution_dumper.pol_dumper.pollution_dumper import PollutionDumper


class SODumper(PollutionDumper):
    logger = logging.getLogger("air_pollution_dumper.SODumper")

    def __init__(self, http_host: str, api_key: str, output_path: str, fs_adapter: FileSystemAdapter):
        PollutionDumper.__init__(self, http_host, api_key, output_path, fs_adapter, SODumper.logger)

    def to_address(self, latitude, longitude, time):
        return "{}/so2/{},{}/{}.json?appid={}".format(self._http_host, latitude, longitude, time, self._api_key)
