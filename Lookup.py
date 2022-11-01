import time

from PrettyResponse import log_pretty_response
from MyLogger import get_my_logger
import requests
from requests.models import Response
import json
import datetime
import re
import KhRequest
import random

url = "https://api.khipu.com/v1/cl/services/dgt.gob.es/appointments/driver-licence/pick-up"
# ulr a escrapear: https://sedeclave.dgt.gob.es/WEB_NCIT_CONSULTA/solicitarCita.faces
headers = {
    "Content-Type": "application/json",
    "x-api-key": "e32d278a-a299-4c0a-8326-b9c8f950fc4f"
}


class NewMessageInResponse(Exception):
    pass


class ErrorNotRecovered(Exception):
    pass


def suggest_filename(response: Response):
    office, country = get_office_and_country(response)
    lookup_status, msg = get_lookup_status(response)
    serial = random.randint(10000, 99999)
    return (f'{response.status_code}-{serial}-{lookup_status} '
            f'O .eq. ({office}) _ C .eq. ({country}) _ M .eq. {msg}')


def get_attr_from_filename() -> [str, str]:
    pass


def get_office_and_country(response: Response):
    json_request = json.loads(response.request.body)
    office = json_request["RequestData"]["Office"]
    country = json_request["RequestData"]["Country"]
    return office, country


def check_for_code(s: str) -> str:
    if '<html>' in s or 'HTML' in s:
        return 'html code'
    elif 'http:' in s or 'HTTP:' in s:
        return 'http code'
    elif len(s) == 0:
        return 'None'
    else:
        return s


def get_lookup_status(response: Response) -> [str, str]:
    """

    :param response:
    :return lookup_status, msg:
    """
    my_logger = get_my_logger()
    if response.status_code == 401:
        msg = check_for_code(response.text)
        my_logger.critical(f'{response.status_code} {msg}')
        return "timeout", msg
    elif response.status_code == 500:
        msg = check_for_code(response.text)
        my_logger.critical(f'500: Internal Server Error with message\n"{msg}"')
        return "timeout", msg
    elif response.status_code == 504:
        msg = check_for_code(response.text)
        my_logger.critical(f'504: Timeout Internal Server Error with message\n"{msg}"')
        return "timeout", msg
    try:
        result: dict = json.loads(response.text)
    except json.JSONDecodeError as e:
        my_logger.critical(f'response no tiene un json válido. Detalles en log de debug')
        my_logger.debug(f'response no tiene un json válido:\n{response.text}')
        raise e
    if isinstance(result, str):
        result = {"Status": "None", "Message": result}
    if "Status" not in result.keys():
        return 'None', ''
    if "FailureReason" not in result.keys():
        result["FailureReason"] = ''
    msg = result["Message"] if "Message" in result.keys() else ''
    if result["FailureReason"] in ["TASK_DUMPED"]:
        lookup_status = "ok"
    elif result["FailureReason"] in ["TASK_EXECUTION_ERROR", "AUTHORIZATION"]:
        lookup_status = "error"
    elif result["FailureReason"] in ["TIMEOUT"]:
        lookup_status = "timeout"
    elif result["FailureReason"] in ["INTERNAL"]:
        lookup_status = "internal"
    elif re.match("El horario de atención al cliente está completo.*", msg):
        lookup_status = "full"
    elif re.match("Estamos recibiendo un número muy elevado de accesos.*", msg):
        lookup_status = "antibot"
    elif re.match("La oficina ingresada no existe.*", msg):
        lookup_status = "office_err"
    elif re.match("El país no existe.*", msg):
        lookup_status = "country_err"
    elif re.match("Unable to download information to initiate payment.*", msg):
        lookup_status = "msg_de_pagos"
    elif result["Status"] == "OK":
        lookup_status = "ok"
    else:
        raise NewMessageInResponse(f'{response.status_code} {msg}')
    return lookup_status, check_for_code(msg)


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


def get_response(country, office, retries_sleep_seconds) -> Response:
    request_data: dict = {
        "RequestData": {
            "Office": office,
            "Country": country,
        },
        #         "CallbackUrl": "https://ranopazo.pythonanywhere.com/log_any/"
    }
    init_time = datetime.datetime.now().replace(microsecond=0)
    response = post_request(url=url, request_data=request_data, request_headers=headers,
                            retries_sleep_seconds=retries_sleep_seconds)
    end_time = datetime.datetime.now().replace(microsecond=0)
    delta_t = end_time - init_time
    KhRequest.save_response(filename=f'{response.status_code} last', response=response)
    log_pretty_response(response=response, delta_t=delta_t)
    return response


def lookup(office: str, country: str, retries_sleep_seconds: int = 10) -> [str, str]:
    get_my_logger().info(f'Request: Horarios para canje de licencia en {office} para {country}')

    response = get_response(country=country, office=office, retries_sleep_seconds=retries_sleep_seconds)

    lookup_status, msg = get_lookup_status(response=response)

    KhRequest.save_response(filename=f'{response.status_code} {lookup_status} - {office} - {country}',
                            response=response)

    return lookup_status, msg
