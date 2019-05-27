import logging
from unittest import TestCase

from air_pollution_dumper.configuration.fs_config import FSConfig
from air_pollution_dumper.parser.dump_parser import parse_co, parse_no, parse_oz, parse_so
from air_pollution_dumper.fs_adapter.default_fs import DefaultFileSystem


class TestParser(TestCase):
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

    def test_co_parser(self):
        data = "  " + '{"time":"2018-12-25T01:41:25Z","location":{"latitude":0,"longitude":0.7226},"data":[{"precision":-4.999999987376214e-07,"pressure":1000,"value":9.278704027337881e-08},{"precision":-4.999999987376214e-07,"pressure":681.2920532226562,"value":1.0947071871214575e-07},{"precision":-4.999999987376214e-07,"pressure":464.15887451171875,"value":1.0778867221006294e-07},{"precision":4.36614868704055e-08,"pressure":316.2277526855469,"value":7.632046816752336e-08},{"precision":1.9522300220842226e-08,"pressure":215.44346618652344,"value":8.424379416283045e-08},{"precision":1.3091818296118163e-08,"pressure":146.77992248535156,"value":8.767751324967321e-08},{"precision":1.1609708749915626e-08,"pressure":100,"value":6.81264538116011e-08},{"precision":1.0210939649368811e-08,"pressure":68.12920379638672,"value":2.0543387435623117e-08},{"precision":8.608719070934967e-09,"pressure":46.415889739990234,"value":1.8953484115513675e-08},{"precision":8.842805598874293e-09,"pressure":31.62277603149414,"value":3.00407805298164e-08},{"precision":9.667605382901456e-09,"pressure":21.544347763061523,"value":9.758478469734655e-09},{"precision":1.2210698230319394e-08,"pressure":14.677992820739746,"value":1.125898396736602e-08},{"precision":1.517793357663777e-08,"pressure":10,"value":3.641343582216905e-08},{"precision":2.1569013242128676e-08,"pressure":6.812920570373535,"value":2.409485411192236e-08},{"precision":2.8708393884357974e-08,"pressure":4.6415886878967285,"value":1.1484728723587523e-08},{"precision":3.8268414215281155e-08,"pressure":3.1622776985168457,"value":8.650146554600724e-08},{"precision":5.405865977081703e-08,"pressure":2.1544346809387207,"value":-7.967953408183348e-09},{"precision":7.163232851326029e-08,"pressure":1.4677993059158325,"value":3.887936017576976e-08},{"precision":9.468482886632046e-08,"pressure":1,"value":1.363242319030178e-07},{"precision":1.4163292405555694e-07,"pressure":0.6812920570373535,"value":-9.208376638980553e-08},{"precision":2.019872198388839e-07,"pressure":0.46415889263153076,"value":1.6834991356518003e-07},{"precision":2.855290972547664e-07,"pressure":0.3162277638912201,"value":3.096133127655776e-07},{"precision":4.190662536984746e-07,"pressure":0.2154434621334076,"value":-5.126558448864671e-07},{"precision":5.840245194121962e-07,"pressure":0.14677992463111877,"value":7.446635095220699e-07},{"precision":6.489067914117186e-07,"pressure":0.10000000149011612,"value":2.8966528020646365e-07},{"precision":9.58769305725582e-07,"pressure":0.04641588777303696,"value":3.5625652117232676e-07},{"precision":1.7358171362502617e-06,"pressure":0.02154434658586979,"value":3.6485912460193504e-06},{"precision":3.4984543617611052e-06,"pressure":0.009999999776482582,"value":7.815624485374428e-06},{"precision":6.331521944957785e-06,"pressure":0.004641588777303696,"value":5.7078409554378595e-06},{"precision":-1.0025875781138893e-05,"pressure":0.002154434798285365,"value":1.0076114449475426e-05},{"precision":-1.5069632354425266e-05,"pressure":0.0010000000474974513,"value":1.7846092305262573e-05},{"precision":-1.9999999494757503e-05,"pressure":0.00046415888937190175,"value":1.4016574823472183e-05},{"precision":-1.9999999494757503e-05,"pressure":0.00021544346236623824,"value":1.4016574823472183e-05},{"precision":-1.9999999494757503e-05,"pressure":9.999999747378752e-05,"value":1.4016574823472183e-05},{"precision":-1.9999999494757503e-05,"pressure":4.641588748199865e-05,"value":1.4016574823472183e-05},{"precision":-1.9999999494757503e-05,"pressure":2.1544346964219585e-05,"value":1.4016574823472183e-05},{"precision":-1.9999999494757503e-05,"pressure":9.999999747378752e-06,"value":1.4016574823472183e-05}]}\n' + "   "
        data = data.encode()
        actual = parse_co(data)
        expected = [5.7078409554378595e-06]
        self.assertEqual(actual, expected)

    def test_so_parser(self):
        data = "  " + '{"time":"2018-12-25T01:41:25Z","location":{"latitude":0,"longitude":0.7233},"data":[{"precision":-9.99999993922529e-09,"pressure":1000,"value":0},{"precision":-9.99999993922529e-09,"pressure":681.2920532226562,"value":0},{"precision":-9.99999993922529e-09,"pressure":464.15887451171875,"value":0},{"precision":-9.21458287450605e-09,"pressure":316.2277526855469,"value":-4.3214840039773605e-10},{"precision":4.192228786337182e-09,"pressure":215.44346618652344,"value":5.174453310274885e-09},{"precision":3.619479160832384e-09,"pressure":146.77992248535156,"value":3.754435873304374e-09},{"precision":2.9572648774234267e-09,"pressure":100,"value":-8.651230842815494e-09},{"precision":4.072716830449963e-09,"pressure":68.12920379638672,"value":3.6584100193692848e-09},{"precision":3.6505529710240125e-09,"pressure":46.415889739990234,"value":2.6752693393916616e-09},{"precision":3.5821077215558716e-09,"pressure":31.62277603149414,"value":-9.944922219062846e-09},{"precision":4.565555045132896e-09,"pressure":21.544347763061523,"value":5.5477982208174126e-09},{"precision":4.74458650145948e-09,"pressure":14.677992820739746,"value":1.788248549239313e-09},{"precision":-5.4295590246056236e-09,"pressure":10,"value":-1.0088703483734918e-10},{"precision":-6.9241319344826024e-09,"pressure":6.812920570373535,"value":-5.383506085365752e-09},{"precision":-7.147510583394023e-09,"pressure":4.6415886878967285,"value":-1.711963570905084e-09},{"precision":-7.76174591265999e-09,"pressure":3.1622776985168457,"value":-1.3853969083044149e-09},{"precision":-8.339783974520287e-09,"pressure":2.1544346809387207,"value":-1.1424290402572979e-09},{"precision":-8.80774297939979e-09,"pressure":1.4677993059158325,"value":-1.2963983220259934e-09},{"precision":-9.134097034291244e-09,"pressure":1,"value":-4.167413081290761e-09},{"precision":-9.99999993922529e-09,"pressure":0.6812920570373535,"value":0},{"precision":-9.99999993922529e-09,"pressure":0.46415889263153076,"value":0},{"precision":-9.99999993922529e-09,"pressure":0.3162277638912201,"value":0},{"precision":-9.99999993922529e-09,"pressure":0.2154434621334076,"value":0},{"precision":-9.99999993922529e-09,"pressure":0.14677992463111877,"value":0},{"precision":-9.99999993922529e-09,"pressure":0.10000000149011612,"value":0},{"precision":-9.99999993922529e-09,"pressure":0.04641588777303696,"value":0},{"precision":-9.99999993922529e-09,"pressure":0.02154434658586979,"value":0},{"precision":-9.99999993922529e-09,"pressure":0.009999999776482582,"value":0},{"precision":-9.99999993922529e-09,"pressure":0.004641588777303696,"value":0.71},{"precision":-9.99999993922529e-09,"pressure":0.002154434798285365,"value":0},{"precision":-9.99999993922529e-09,"pressure":0.0010000000474974513,"value":0},{"precision":-9.99999993922529e-09,"pressure":0.00046415888937190175,"value":0},{"precision":-9.99999993922529e-09,"pressure":0.00021544346236623824,"value":0},{"precision":-9.99999993922529e-09,"pressure":9.999999747378752e-05,"value":0},{"precision":-9.99999993922529e-09,"pressure":4.641588748199865e-05,"value":0},{"precision":-9.99999993922529e-09,"pressure":2.1544346964219585e-05,"value":0},{"precision":-9.99999993922529e-09,"pressure":9.999999747378752e-06,"value":0}]}\n' + "   "
        data.encode()
        actual = parse_so(data)
        print(actual)
        expected = [0.71]
        self.assertEqual(actual, expected)

    def test_no_parser(self):
        data = "  " + '{"time":"2017-02-17T14:35:04Z","location":{"latitude":0.9037,"longitude":-1.0239},"data":{"no2":{"precision":8.24037995446272e+14,"value":1.809560184553472e+15},"no2_strat":{"precision":2.00000000753664e+14,"value":1.727748842192896e+15},"no2_trop":{"precision":9.05144157863936e+14,"value":8.1811384303616e+13}}}\n' + "   "
        actual = parse_no(data)
        expected = [1809560184553472.0]
        self.assertEqual(actual, expected)

    def test_oz_parser(self):
        data = "  " + '{"time":"2017-04-23T13:39:51Z","location":{"latitude":1.2811,"longitude":-0.4828},"data":276.9101257324219}\n' + "   "
        data = data.encode()
        actual = parse_oz(data)
        expected = [276.9101257324219]
        self.assertEqual(actual, expected)
