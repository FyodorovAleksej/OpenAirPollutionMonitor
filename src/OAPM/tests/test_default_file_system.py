import logging
from unittest import TestCase

from air_pollution_dumper.configuration.fs_config import FSConfig
from air_pollution_dumper.fs_adapter.default_fs import DefaultFileSystem


class TestDefaultFileSystem(TestCase):
    TEST_DIR = "test_out/"

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

    def setUp(self):
        super().setUp()
        self.__config = FSConfig(TestDefaultFileSystem.TEST_DIR, None)
        self.__adapter = DefaultFileSystem(self.__config)
        self.__adapter.mkdir("")

    def test_write_file(self):
        data = """
        Some test data
        anything else
        and also this one
        so, it is the end
        tests, tests never change
        """
        self.__adapter.write_file("test_write.txt", data)
        file = open(TestDefaultFileSystem.TEST_DIR + "test_write.txt", "r")
        actual = file.read()
        file.close()
        self.assertEqual(data, actual)

    def test_append_to_file(self):
        data = """
        Some classic lines
        Or something different
        """
        self.__adapter.write_file("test_append.txt", data)
        append = """
        Something also different
        Not empty line
        """
        self.__adapter.append_to_file("test_append.txt", append)
        actual = self.__adapter.read_file("test_append.txt")
        self.assertEqual(data + append, actual)

    def test_remove_file(self):
        files = [i for i in self.__adapter.ls("") if str(i).endswith(".txt")]
        past = files[1:]
        self.__adapter.remove_file(files[0])
        actual = [i for i in self.__adapter.ls("") if str(i).endswith(".txt")]
        self.assertEqual(past, actual)

    def test_read_file(self):
        file = open(TestDefaultFileSystem.TEST_DIR + "test_read.txt", "w")
        data = """
        Oh, here we go again
        I so tired to wrote this lines...
        help me please :)  
        """
        file.write(data)
        file.flush()
        file.close()
        actual = self.__adapter.read_file("test_read.txt")
        self.assertEqual(data, actual)

    def test_is_exist(self):
        file = open(TestDefaultFileSystem.TEST_DIR + "test_exist.txt", "w")
        file.write("")
        file.flush()
        file.close()
        self.assertTrue(self.__adapter.is_exist("test_exist.txt"))
