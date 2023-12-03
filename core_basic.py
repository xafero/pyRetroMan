import json
from os import getcwd
from os.path import isfile, join


def get_current_dir(input_dir=None):
    if input_dir is None:
        input_dir = getcwd()
    return input_dir


def write_as_json(file_name, content):
    with open(file_name, "w") as f:
        json.dump(content, f, indent=4)
    return content


def load_dict_if_exists(filename, func=None, input_dir=None):
    store_root = get_current_dir(input_dir)
    store_file = join(store_root, f"{filename}.json")
    content = dict()
    if isfile(store_file):
        with open(store_file, "r") as f:
            content = json.load(f)
    if func is not None:
        content = write_as_json(store_file, func(content))
    return content
