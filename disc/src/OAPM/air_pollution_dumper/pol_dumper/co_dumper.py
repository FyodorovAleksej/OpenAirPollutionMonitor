import logging

from air_pollution_dumper.fs_adapter.adapter import FileSystemAdapter
from air_pollution_dumper.pol_dumper.pollution_dumper import PollutionDumper


class CODumper(PollutionDumper):
    logger = logging.getLogger("air_pollution_dumper.CODumper")

    def __init__(self, http_host: str, api_key: str, output_path: str, fs_adapter: FileSystemAdapter):
        PollutionDumper.__init__(self, http_host, api_key, output_path, fs_adapter, CODumper.logger)

    def to_address(self, latitude, longitude, time):
        return "{}/co/{},{}/{}.json?appid={}".format(self._http_host, latitude, longitude, time, self._api_key)

    def dump(self, latitude, longitude, time):
        return super().dump(latitude, longitude, time)
