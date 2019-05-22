# -*- coding: utf-8 -*-

"""Console script for OpenAirPolutionMonitor."""
import sys
from configparser import ConfigParser

import click

from configuration.application_config import ApplicationConfig
from dumper import dump_parser as dp
from dumper.co_dumper import CODumper
from dumper.fs_adapter.default_fs import DefaultFileSystem
from dumper.no_dumper import NODumper
from dumper.oz_dumper import OZDumper
from dumper.pollution_dumper import PollutionDumper
from dumper.so_dumper import SODumper
from fs_adapter.distributed_fs import DistributedFileSystem


@click.command()
@click.option('--config', '-c', default="./config/dumper_config.ini",
              help='path to dumper config.')
def main(config):
    config_parser = ConfigParser()
    config_parser.read(config)

    app_config = ApplicationConfig.parse_from_file(config)

    api_cfg = app_config.get_api_config()
    fs_config = app_config.get_fs_config()
    kafka_config = app_config.get_kafka_config()

    fs = DefaultFileSystem(fs_config) if fs_config.get_host() is None else DistributedFileSystem(fs_config)

    co_dumper = CODumper(api_cfg.get_host(), api_cfg.get_api_key(), "co/", fs)
    so_dumper = SODumper(api_cfg.get_host(), api_cfg.get_api_key(), "so/", fs)
    no_dumper = NODumper(api_cfg.get_host(), api_cfg.get_api_key(), "no/", fs)
    oz_dumper = OZDumper(api_cfg.get_host(), api_cfg.get_api_key(), "oz/", fs)

    fs.mkdir("")

    sender = None
    for latitude in range(0, 180):
        for longitude in range(0, 180):
            for year in range(2015, 2019):
                key = fs.to_file_path("", latitude, longitude, year)
                send_dump(co_dumper, sender, app_config.get_additional_configs()["TOPICS"]["CO_TOPIC"], key, latitude,
                          longitude, year, dp.parse_co)
                send_dump(so_dumper, sender, app_config.get_additional_configs()["TOPICS"]["SO_TOPIC"], key, latitude,
                          longitude, year, dp.parse_so)
                send_dump(oz_dumper, sender, app_config.get_additional_configs()["TOPICS"]["OZ_TOPIC"], key, latitude,
                          longitude, year, dp.parse_oz)
                send_dump(no_dumper, sender, app_config.get_additional_configs()["TOPICS"]["NO_TOPIC"], key, latitude,
                          longitude, year, dp.parse_no)


def send_dump(value_dumper: PollutionDumper, sender, topic, key, latitude, longitude, year, parser):
    try:
        data = value_dumper.dump(latitude, longitude, str(year) + "Z")
        print(topic, " -----", data)
    except ConnectionError:
        print(topic, " no data")
    # value = parser(data)
    # for val in value:
    #    sender.send_message(topic, str(val), key)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
