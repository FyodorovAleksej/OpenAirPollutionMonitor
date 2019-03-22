# -*- coding: utf-8 -*-

"""Console script for OpenAirPolutionMonitor."""
import sys
from configparser import ConfigParser

import click

from dumper.co_dumper import CODumper
from dumper.fs_adapter.default_fs import DefaultFileSystem


@click.command()
@click.option('--config', '-c', default="./config/dumper_config.ini",
              help='path to dumper config.')
def main(config):
    config_parser = ConfigParser()
    config_parser.read(config)

    api_cfg = dict(config_parser["WEATHER_MAP_CONFIG"])
    fs_config = dict(config_parser["FS_CONFIG"])

    out = fs_config["dumper_output_path"]
    co_dumper = CODumper(api_cfg["api_host"], api_cfg["api_key"], "", DefaultFileSystem())
    fs = DefaultFileSystem()

    fs.mkdir(out)

    ser_str = str(kafka_config["servers"])
    servers = ser_str.split(",") if "," in ser_str else [ser_str]

    sender = KafkaSender(servers)
    for latitude in range(0, 20):
        for longitude in range(0, 20):
            for year in range(2016, 2019):
                path = fs.to_file_path(out, latitude, longitude, year)
                if not (fs.is_exist(path)):
                    data = path #co_dumper.dump(latitude, longitude, str(year) + "Z")
                    #fs.write_file(path, data)
                    sender.send_message(kafka_config["co_topic"], data, str(year))


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
