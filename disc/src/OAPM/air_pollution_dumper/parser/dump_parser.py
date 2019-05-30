import json


def parse_co(json_data):
    json_temp = json_data[2:-3]
    data = json.loads(json_temp)
    entities = data["data"]
    res = []
    if entities is not None:
        for entity in entities:
            pressure = float(entity["pressure"])
            if 0.003 < pressure <= 0.007:
                res.append(entity["value"])
    return res


def parse_so(json_data):
    json_temp = json_data[2:-3]
    data = json.loads(json_temp)
    entities = data["data"]
    res = []
    if entities is not None:
        for entity in entities:
            pressure = float(entity["pressure"])
            if 0.003 < pressure <= 0.007:
                res.append(entity["value"])
    return res


def parse_oz(json_data):
    json_temp = json_data[2:-3]
    data = json.loads(json_temp)
    res = []
    if data is not None:
        res.append(data["data"])
    return res


def parse_no(json_data):
    json_temp = json_data[2:-3]
    data = json.loads(json_temp)
    res = []
    entities = data["data"]
    if entities is not None:
        values = entities["no2"]
        if values is not None:
            res.append(values["value"])
    return res
