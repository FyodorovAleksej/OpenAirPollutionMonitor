# -*- coding: utf-8 -*-

"""Console script for OpenAirPolutionMonitor."""
import logging
import sys
from configparser import ConfigParser

import click

from air_pollution_dumper.configuration.application_config import ApplicationConfig
from air_pollution_dumper.parser import dump_parser as dp
from air_pollution_dumper.pol_dumper.co_dumper import CODumper
from air_pollution_dumper.fs_adapter.default_fs import DefaultFileSystem
from air_pollution_dumper.pol_dumper.no_dumper import NODumper
from air_pollution_dumper.pol_dumper.oz_dumper import OZDumper
from air_pollution_dumper.pol_dumper.pollution_dumper import PollutionDumper
from air_pollution_dumper.pol_dumper.so_dumper import SODumper
from air_pollution_dumper.fs_adapter.distributed_fs import DistributedFileSystem

logger = logging.getLogger("cli")


@click.command()
@click.option('--config', '-c', default="./config/dumper_config.ini",
              help='path to air_pollution_dumper config.')
def main(config):
    config_parser = ConfigParser()
    config_parser.read(config)

    app_config = ApplicationConfig.parse_from_file(config)

    api_cfg = app_config.get_api_config()
    fs_config = app_config.get_fs_config()
    kafka_config = app_config.get_kafka_config()

    logger_config = app_config.get_additional_configs()["LOGGER"]
    init_logger(logger_config)

    logger.info("****** air_pollution_dumper was started *******")
    logger.info("****** air_pollution_dumper configs: **********")
    logger.info(app_config)
    logger.info("*********************************")

    logger.info("Create file system adapter")
    fs = DefaultFileSystem(fs_config) if fs_config.get_host() is None else DistributedFileSystem(fs_config)

    co_dumper = CODumper(api_cfg.get_host(), api_cfg.get_api_key(), "co/", fs)
    so_dumper = SODumper(api_cfg.get_host(), api_cfg.get_api_key(), "so/", fs)
    no_dumper = NODumper(api_cfg.get_host(), api_cfg.get_api_key(), "no/", fs)
    oz_dumper = OZDumper(api_cfg.get_host(), api_cfg.get_api_key(), "oz/", fs)

    logger.info("Create output diretory")
    fs.mkdir("")

    sender = None
    for latitude in range(0, 180):
        for longitude in range(0, 180):
            for year in range(2015, 2019):
                key = fs.to_file_path("", latitude, longitude, year)
                logger.info("Processing for key = " + key)
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
        logger.info("Trying get data for topic = {}, latitude = {}, longitude = {}, year = {}".format(topic, latitude, longitude, year))
        data = value_dumper.dump(latitude, longitude, str(year) + "Z")
    except ConnectionError as e:
        logger.warning("Data wasn't founded : {}".format(e))
    # value = parser(data)
    # for val in value:
    #    sender.send_message(topic, str(val), key)


def init_logger(logger_config: dict):
    file_handler = logging.FileHandler(logger_config["FILE"])
    stderr_handler = logging.StreamHandler()
    logging.basicConfig(format='%(asctime)s [%(levelname)s] <%(name)s> - %(message)s',
                        handlers=[file_handler, stderr_handler],
                        level=logger_config["LEVEL"].upper())


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
