import pickle
from requests.models import Response
from requests.exceptions import RequestException
import requests
from unittest.mock import Mock


def save_response(file_name: str, response):
    dir_name = f'var/responses'
    file_name = f'{dir_name}/{file_name.replace("/", "")}.response'
    with open(file=file_name, mode='wb') as f:
        pickle.dump(file=f, obj=response, protocol=pickle.HIGHEST_PROTOCOL)


def load_response(file_name: str) -> Response:
    with open(file=file_name, mode='rb') as f:
        response = pickle.load(file=f)
    return response


def mock_request_post(file_name: str) -> [str, str]:
    response = load_response(file_name=file_name)
    requests.post = Mock()
    requests.post.return_value = response
    office = 'mocked_office'
    country = 'mocked_country'
    return office, country


def mock_exception_RequestException(file_name: str) -> [str, str]:
    """
    All exceptions that Requests explicitly raises inherit from requests.exceptions.RequestException.
        In the event of a network problem (e.g. DNS failure, refused connection, etc),
        Requests will raise a ConnectionError exception.

        In the event of the rare invalid HTTP response, Requests will raise an HTTPError exception.

        If a request times out, a Timeout exception is raised.

        If a request exceeds the configured number of maximum redirections, a TooManyRedirects exception is raised.
    """
    response = load_response(file_name=file_name)
    requests.post = Mock()
    requests.post.side_effect = RequestException('MockedRequestException()')
    requests.post.return_value = response
    office = 'mocked_office'
    country = 'mocked_country'
    return office, country


def mock_post_of_request_to_test():
    mock_response = Mock()
    mock_response.text = 'Soy un texto moqueado que reemplaza text del post :-)'
    requests.post = Mock()
    requests.post.return_value = mock_response
    return


def post_request_to_test() -> Response:
    url = 'https://www.emol.com/'
    print(f'Buscando cuerpo de {url}')
    response = requests.post(url, json="", headers="")
    print('Respuesta recibida:')
    print(response.text)
    return response
