import logging
from unittest import TestCase

from air_pollution_dumper.configuration.fs_config import FSConfig
from air_pollution_dumper.fs_adapter.default_fs import DefaultFileSystem
from air_pollution_dumper.pol_dumper.co_dumper import CODumper
from air_pollution_dumper.pol_dumper.no_dumper import NODumper
from air_pollution_dumper.pol_dumper.oz_dumper import OZDumper
from air_pollution_dumper.pol_dumper.so_dumper import SODumper


class TestDumper(TestCase):
    def setUp(self):
        self.__config = FSConfig("test_out/", None)
        self.__adapter = DefaultFileSystem(self.__config)

    @classmethod
    def setUpClass(cls):
        conf = {"FILE": "tests.log", "LEVEL": "debug"}
        file_handler = logging.FileHandler(conf["FILE"])
        stderr_handler = logging.StreamHandler()
        logging.basicConfig(format='%(asctime)s [%(levelname)s] <%(name)s> - %(message)s',
                            handlers=[file_handler, stderr_handler],
                            level=conf["LEVEL"].upper())
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        logging.shutdown()
        super().tearDownClass()

    def test_co_address(self):
        co_dumper = CODumper("some_host", "atztpcnk", "test", self.__adapter)
        actual = co_dumper.to_address(25, 45, 2017)
        expected = "some_host/co/25,45/2017.json?appid=atztpcnk"
        self.assertEqual(actual, expected)

    def test_so_address(self):
        so_dumper = SODumper("some_host", "atztpcnk", "test", self.__adapter)
        actual = so_dumper.to_address(38, 92, 2017)
        expected = "some_host/so2/38,92/2017.json?appid=atztpcnk"
        self.assertEqual(actual, expected)

    def test_no_address(self):
        no_dumper = NODumper("some_host", "atztpcnk", "test", self.__adapter)
        actual = no_dumper.to_address(91, 23, 2018)
        expected = "some_host/no2/91,23/2018.json?appid=atztpcnk"
        self.assertEqual(actual, expected)

    def test_oz_address(self):
        oz_dumper = OZDumper("some_host", "atztpcnk", "test", self.__adapter)
        actual = oz_dumper.to_address(106, 22, 2016)
        expected = "some_host/o3/106,22/2016.json?appid=atztpcnk"
        self.assertEqual(actual, expected)
