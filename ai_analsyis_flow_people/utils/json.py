import json


def read_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data