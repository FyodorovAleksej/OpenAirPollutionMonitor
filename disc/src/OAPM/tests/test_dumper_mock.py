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

    def test_co_dumper(self):
        co_dumper = CODumper("some_host", "atztpcnk", "test_dump_co", self.__adapter)
        co_dumper.set_request_method(mock_co_request)
        cont = co_dumper.dump(25, 45, 2017)
        self.assertEqual(cont, "Yes, it's ok")

    def test_so_dumper(self):
        so_dumper = SODumper("some_host", "atztpcnk", "test_dump_so", self.__adapter)
        so_dumper.set_request_method(mock_so_request)
        cont = so_dumper.dump(30, 91, 2016)
        self.assertEqual(cont, "Yes, it's ok")

    def test_no_dumper(self):
        no_dumper = NODumper("some_host", "atztpcnk", "test_dump_no", self.__adapter)
        no_dumper.set_request_method(mock_no_request)
        cont = no_dumper.dump(28, 49, 2015)
        self.assertEqual(cont, "Yes, it's ok")

    def test_oz_dumper(self):
        oz_dumper = OZDumper("some_host", "atztpcnk", "test_dump_oz", self.__adapter)
        oz_dumper.set_request_method(mock_oz_request)
        cont = oz_dumper.dump(24, 92, 2018)
        self.assertEqual(cont, "Yes, it's ok")


def mock_co_request(address):
    if address == "some_host/co/25,45/2017.json?appid=atztpcnk":
        return ResponseMock(200, "Yes, it's ok")
    return ResponseMock(400, "Something wrong")


def mock_so_request(address):
    if address == "some_host/so2/30,91/2016.json?appid=atztpcnk":
        return ResponseMock(200, "Yes, it's ok")
    return ResponseMock(400, "Something wrong")


def mock_no_request(address):
    if address == "some_host/no2/28,49/2015.json?appid=atztpcnk":
        return ResponseMock(200, "Yes, it's ok")
    return ResponseMock(400, "Something wrong")


def mock_oz_request(address):
    if address == "some_host/o3/24,92/2018.json?appid=atztpcnk":
        return ResponseMock(200, "Yes, it's ok")
    return ResponseMock(400, "Something wrong")


class ResponseMock:
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content
