# OpenAirPolutionMonitor
open application for monitoring air polution

# STEPS:

1. build OAPSpark from sources by gradle docker:

$ cd ./src/OAPSpark/
$ ./rebuild.sh
$ cd -

2. Set your API Key in config file (./src/OAPM/config/dumper_config.ini)

3. Run cluster:

$ cd ./src/docker/
$ docker-compose up

4. Open localhost:8090 and waiting for connecting

5. OPen and rerun 'spark' notebook
