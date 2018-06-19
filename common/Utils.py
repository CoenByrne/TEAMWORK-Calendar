import json


def bytes_to_json(data):
    my_json = data.decode('utf8').replace("'", '"')
    # print(my_json)

    # Load the JSON to a Python list & dump it back out as formatted JSON
    data = json.loads(my_json)
    s = json.dumps(data, indent=4, sort_keys=True)

    dic = json.loads(my_json)
    return dic

