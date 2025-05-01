import json


def load_json(full_path):
    with open(full_path, 'r', encoding='utf-8') as file:
        json_string = file.read()
        return json.loads(json_string)