import pickle
import time

import requests
from requests.exceptions import RequestException
from requests.models import Response
from unittest.mock import Mock
from pathlib import Path
import json
from MyLogger import get_my_logger
from datetime import timedelta


class ErrorNotRecovered(Exception):
    pass


def sfix(s: str, l: int) -> str:
    aux = f'{s:.<{l}}'[0:l]
    return aux


def save_response(filename: str, response: Response):
    filename = Path(f'{filename}.response')
    with open(file=filename, mode='wb') as f:
        pickle.dump(file=f, obj=response)


def load_response(file_name: str) -> Response:
    with open(file=file_name, mode='rb') as f:
        response = pickle.load(file=f)
    return response


def mock_response(file_name: str) -> Response:
    response = load_response(file_name=file_name)
    requests.post = Mock()
    requests.post.return_value = response
    return response


def mock_post(response: Response):
    requests.post = Mock()
    requests.post.return_value = response
    return


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


def indent_text(text: str, indent: str) -> str:
    result = []
    for line in text.splitlines():
        result.append(f'{indent}{line}')
    return '\n'.join(result)


def indent_dict(json_dict: dict, cut_border=False) -> str:
    text = json.dumps(json_dict, indent='\t', ensure_ascii=False)
    if cut_border:
        text = text.splitlines()
        result = []
        for i in range(len(text) - 2):
            result.append(text[i + 1])
        text = "\n".join(result)
    if text[0] != '\t':
        text = indent_text(text, '\t')
    return text


def indent_str(json_str: str, cut_border=False) -> str:
    try:
        json_dict = json.loads(json_str)
        text = indent_dict(json_dict=json_dict, cut_border=cut_border)
    except (TypeError, json.decoder.JSONDecodeError):
        text = f'\t{json_str}'
    return text


def get_pretty_response(response: Response, delta_t: timedelta = None) -> str:
    """
    Retorna una representación en texto preparada para una visualización humana de un response.
    :param response: from requests.models import Response.
    :param delta_t: Opcional. Tiempo que tomó recibir la respuesta.
    :return: response formateada como texto.
    """
    assert (response is not None)
    delta_str = f' (delta_t = {delta_t})' if delta_t is not None else ""

    result = (
        f'{response.status_code} Petición {response.request.method} a {response.url}{delta_str}\n'
        f'--->\n'
        f'{indent_dict(json_dict=dict(response.request.headers), cut_border=True)}\n'
        f'\t---\n'
        f'{indent_str(json_str=response.request.body, cut_border=False)}\n'
        f'<---\n'
        f'{indent_dict(json_dict=dict(response.headers), cut_border=True)}\n'
        f'\t---\n'
        f'{indent_str(json_str=response.text, cut_border=False)}\n'
        f'\nORIGINAL RESPONSE BODY:\n{response.text}\n\n'
    )
    return result


def log_pretty_response(response: Response, delta_t: timedelta = None):
    assert (response is not None)
    my_logger = get_my_logger()

    formatted_response = get_pretty_response(response=response, delta_t=delta_t)
    my_logger.debug(formatted_response)


def post_request(url: str, request_data: dict, request_headers, retries_sleep_seconds=10) -> Response:
    my_logger = get_my_logger()
    available_retries = 5
    retry = True
    while retry and available_retries > -1:
        retry = False
        try:
            response = requests.post(url, json=request_data, headers=request_headers)
        except requests.exceptions.RequestException as e:
            if available_retries:
                my_logger.info(f'requests.exceptions.ConnectionError: {e}')
                my_logger.info(f'sleeping {retries_sleep_seconds} seconds. {available_retries} available retries...')
                time.sleep(retries_sleep_seconds)
                available_retries -= 1
                retry = True
            else:
                error_msg = (f'No quedan reintentos disponibles para recuperarse de un error.\n'
                             f'Y se recibió:\n{e}')
                my_logger.critical(error_msg)
                raise ErrorNotRecovered(error_msg)
    return response