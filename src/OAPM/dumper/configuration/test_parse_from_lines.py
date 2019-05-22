from unittest import TestCase
import dumper.configuration.api_config as api
import dumper.configuration.fs_config as fs
import dumper.configuration.kafka_producer_config as kafka

class TestParse_from_lines(TestCase):
    def test_parse_from_lines(self):
        lines = [
            "API_host   :   222011.23343",
            "api_KEY : 222111"
        ]
        print(api.parse_from_lines(lines))
        #self.fail()
