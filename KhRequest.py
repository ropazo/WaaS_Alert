import pickle
import time

import requests
from requests.models import Response
from pathlib import Path

from BasicFormats import indent_dict, indent_str
from MyLogger import get_my_logger
from datetime import timedelta


class ErrorNotRecovered(Exception):
    pass


def save_response(filename: str, response: Response):
    filename = Path(f'{filename}.response')
    with open(file=filename, mode='wb') as f:
        pickle.dump(file=f, obj=response)


def load_response(filename: str) -> Response:
    with open(file=filename, mode='rb') as f:
        response = pickle.load(file=f)
    return response


def format_pretty_response(response: Response, delta_t: timedelta = None) -> str:
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

    formatted_response = format_pretty_response(response=response, delta_t=delta_t)
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


