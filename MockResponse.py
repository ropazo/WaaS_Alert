import random
import time
from unittest.mock import Mock, MagicMock

import requests
from requests import Response

import Files
import KhRequest as kr
import Lookup

from KhRequest import load_response


def mock_post_with_response(filename: str) -> Response:
    response = load_response(filename=filename)
    requests.post = Mock()
    requests.post.return_value = response
    return response


def mock_post_with_random_response(response: Response) -> Response:
    requests.post = Mock()
    requests.post.return_value = response
    return response


def mock_post_with_exception(response: Response, mocked_exception):
    """
    All exceptions that Requests explicitly raises inherit from requests.exceptions.RequestException.
        In the event of a network problem (e.g. DNS failure, refused connection, etc),
        Requests will raise a ConnectionError exception.

        In the event of the rare invalid HTTP response, Requests will raise an HTTPError exception.

        If a request times out, a Timeout exception is raised.

        If a request exceeds the configured number of maximum redirections, a TooManyRedirects exception is raised.
    """
    requests.post = Mock()
    requests.post.side_effect = mocked_exception
    requests.post.return_value = response
    return


def post_request_to_test() -> Response:
    url = 'https://www.emol.com/'
    print(f'Buscando cuerpo de {url}')
    response = requests.post(url, json="", headers="")
    print('Respuesta recibida:')
    print(response.text)
    return response


def wait_and_get_random_response(*args, **kwargs):
    time.sleep(random.randint(1000, 9999)/10000)
    path = 'etc/tests/responses/selected'
    response_files = Files.get_files_from_path(path)
    filename = response_files[random.randint(0, len(response_files)-1)]
    full_filename = f'{path}/{filename}'
    response = kr.load_response(filename=full_filename)
    return response


def mock_request_post(filename: str) -> [str, str]:
    response = kr.load_response(filename=filename)
    office, country = Lookup.get_office_and_country(response=response)
    requests.post = Mock()
    requests.post.return_value = response
    return office, country


def mock_request_post_with_random_response():
    mock = MagicMock()
    mock.side_effect = wait_and_get_random_response
    requests.post = mock
    return
