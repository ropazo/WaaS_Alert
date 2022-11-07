import os
from os.path import isfile, join


def get_files_from_path(path):
    response_files = [f for f in os.listdir(path) if isfile(join(path, f))]
    return response_files