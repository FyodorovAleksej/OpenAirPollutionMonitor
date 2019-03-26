# -*- coding: utf-8 -*-

"""Console script for OpenAirPolutionMonitor."""
import sys
from configparser import ConfigParser

import click

from dumper import dump_parser as dp
from dumper.co_dumper import CODumper
from dumper.fs_adapter.default_fs import DefaultFileSystem
from dumper.kafka_adapter.kafka_adapter import KafkaSender
from dumper.no_dumper import NODumper
from dumper.oz_dumper import OZDumper
from dumper.pollution_dumper import PollutionDumper
from dumper.so_dumper import SODumper


@click.command()
@click.option('--config', '-c', default="./config/dumper_config.ini",
              help='path to dumper config.')
def main(config):
    config_parser = ConfigParser()
    config_parser.read(config)

    api_cfg = dict(config_parser["WEATHER_MAP_CONFIG"])
    fs_config = dict(config_parser["FS_CONFIG"])
    kafka_config = dict(config_parser["KAFKA_CONFIG"])

    out = fs_config["dumper_output_path"]
    co_dumper = CODumper(api_cfg["api_host"], api_cfg["api_key"], "", DefaultFileSystem())
    so_dumper = SODumper(api_cfg["api_host"], api_cfg["api_key"], "", DefaultFileSystem())
    no_dumper = NODumper(api_cfg["api_host"], api_cfg["api_key"], "", DefaultFileSystem())
    oz_dumper = OZDumper(api_cfg["api_host"], api_cfg["api_key"], "", DefaultFileSystem())
    fs = DefaultFileSystem()

    fs.mkdir(out)

    ser_str = str(kafka_config["servers"])
    servers = ser_str.split(",") if "," in ser_str else [ser_str]

    sender = KafkaSender(servers)
    for latitude in range(0, 20):
        for longitude in range(0, 20):
            for year in range(2016, 2019):
                path = fs.to_file_path(out, latitude, longitude, year)
                key = fs.to_file_path("", latitude, longitude, year)
                if not (fs.is_exist(path)):
                    send_dump(co_dumper, sender, kafka_config["co_topic"], key, latitude, longitude, year, dp.parse_co)
                    send_dump(so_dumper, sender, kafka_config["so_topic"], key, latitude, longitude, year, dp.parse_so)
                    send_dump(oz_dumper, sender, kafka_config["oz_topic"], key, latitude, longitude, year, dp.parse_oz)
                    send_dump(no_dumper, sender, kafka_config["no_topic"], key, latitude, longitude, year, dp.parse_no)


def send_dump(value_dumper: PollutionDumper, sender, topic, key, latitude, longitude, year, parser):
    data = value_dumper.dump(latitude, longitude, str(year) + "Z")
    value = parser(data)
    for val in value:
        sender.send_message(topic, str(val), key)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
