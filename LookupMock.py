import time
import os
from os.path import isfile, join
import requests
from unittest.mock import Mock
from requests import Response
import Lookup
from KhRequest import load_response
import random


def wait_for_response(max_seconds: int, response: Response):
    time.sleep(random.randint(1, max_seconds))
    return response


def mock_request_post(filename: str) -> [str, str]:
    response = load_response(filename=filename)
    office, country = Lookup.get_office_and_country(response=response)
    requests.post = Mock()
    requests.post.return_value = response
    return office, country


def mock_request_post_with_random_response(path: str) -> [str, str]:
    response_files = [f for f in os.listdir(path) if isfile(join(path, f))]
    filename = response_files[random.randint(0, len(response_files))]
    print(filename)
    full_filename = f'{path}/{filename}'
    response = load_response(filename=full_filename)
    office, country = Lookup.get_office_and_country(response=response)
    requests.post = Mock()
    requests.post.side_effect = wait_for_response(max_seconds=3, response=response)
    return office, country


