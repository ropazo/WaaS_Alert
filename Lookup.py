from datetime import datetime
import requests
from KhRequest import log_pretty_response, post_request
from MyLogger import get_my_logger
from requests.models import Response
import json
import datetime
import re
import KhRequest as kr
from BasicFormats import sfix
import random
import time
import unittest.mock

url = "https://api.khipu.com/v1/cl/services/dgt.gob.es/appointments/driver-licence/pick-up"
# ulr a escrapear: https://sedeclave.dgt.gob.es/WEB_NCIT_CONSULTA/solicitarCita.faces
headers = {
    "Content-Type": "application/json",
    "x-api-key": "e32d278a-a299-4c0a-8326-b9c8f950fc4f"
}


class NewMessageInResponse(Exception):
    pass


def suggest_filename(response: Response):
    office, country = get_office_and_country(response)
    lookup_status, msg = get_lookup_status(response)
    serial = random.randint(1000000, 9999999)
    suggested = (f'{response.status_code} {sfix(lookup_status, 8)}   '
                    f'{sfix(office, 30)}  {sfix(country, 12)}   msg={sfix(msg, 60)}  uid={serial}')
    suggested = suggested.replace('"', '-')
    suggested = suggested.replace('/', '-')

    return suggested


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
    my_logger = get_my_logger()
    if response.status_code == 401:
        msg = check_for_code(response.text)
        my_logger.critical(f'{response.status_code} {msg}')
        return "timeout", msg
    elif response.status_code == 500:
        msg = check_for_code(response.text)
        my_logger.critical(f'500: Internal Server Error with message\n"{msg}"')
        return "timeout1", msg
    elif response.status_code == 504:
        msg = check_for_code(response.text)
        my_logger.critical(f'504: Timeout Internal Server Error with message\n"{msg}"')
        return "timeout2", msg
    try:
        result: dict = json.loads(response.text)
    except json.JSONDecodeError as e:
        my_logger.critical(f'response no tiene un json válido. Detalles en log de debug')
        my_logger.debug(f'response no tiene un json válido:\n{response.text}')
        raise e
    except TypeError as e:
        if isinstance(response.text, unittest.mock.Mock) or isinstance(response.text, unittest.mock.MagicMock):
            print('Así las cosas')
        else:
            my_logger.debug(f'type(response.text): {type(response.text)}')
            my_logger.debug(f'response.text:\n{response.text}')
            raise e
    except BaseException as e:
        print(f'Otra excepción: {e}')
        raise e
    if isinstance(result, str):
        result = {"Status": "None", "Message": result}
    if "Status" not in result.keys():
        return 'None', ''
    if "FailureReason" not in result.keys():
        result["FailureReason"] = ''
    msg = result["Message"] if "Message" in result.keys() else ''
    if result["FailureReason"] in ["TASK_DUMPED"]:
        lookup_status = "dump"
    elif result["FailureReason"] in ["TASK_EXECUTION_ERROR", "AUTHORIZATION"]:
        lookup_status = "error"
    elif result["FailureReason"] in ["TIMEOUT"]:
        lookup_status = "timeout"
    elif result["FailureReason"] in ["INTERNAL"]:
        lookup_status = "internal"
    elif re.match("El horario de atención al cliente está completo.*", msg):
        lookup_status = "full"
    elif re.match("Estamos recibiendo un número muy elevado de accesos.*", msg):
        lookup_status = "overload"
    elif re.match("La oficina ingresada no existe.*", msg):
        lookup_status = "office_err"
    elif re.match("El país no existe.*", msg):
        lookup_status = "country_err"
    elif re.match("Unable to download information to initiate payment.*", msg):
        lookup_status = "msg_de_pagos"
    elif re.match("Tipo de trámite no disponible.*", msg):
        lookup_status = "trámite no disponible"
    elif result["Status"] == "OK":
        lookup_status = "ok"
    else:
        raise NewMessageInResponse(f'{response.status_code} {msg}')
    return lookup_status, check_for_code(msg)


def get_response(country, office, retries_sleep_seconds) -> Response:
    request_data: dict = {
        "RequestData": {
            "Office": office,
            "Country": country,
        },
        #         "CallbackUrl": "https://ranopazo.pythonanywhere.com/log_any/"
    }
    init_time = datetime.datetime.now().replace(microsecond=0)
    my_logger = get_my_logger()
    available_retries = 5
    retry = True
    while retry and available_retries > -1:
        retry = False
        response = post_request(url=url, request_data=request_data, request_headers=headers,
                                retries_sleep_seconds=retries_sleep_seconds)
        end_time = datetime.datetime.now().replace(microsecond=0)
        lookup_status, msg = get_lookup_status(response=response)
        if lookup_status == 'dump':
            if available_retries:
                my_logger.info(f'Se recibió un dump')
                my_logger.info(f'sleeping {retries_sleep_seconds} seconds. {available_retries} available retries...')
                time.sleep(retries_sleep_seconds)
                available_retries -= 1
                retry = True
            else:
                my_logger.critical(f'Se recibió un dump y ya no quedan reintentos disponibles.')
    delta_t = end_time - init_time
    kr.save_response(filename=f'./var/responses/{response.status_code} last', response=response)
    log_pretty_response(response=response, delta_t=delta_t)
    return response


def lookup(office: str, country: str, max_waiting_time: int = 10) -> [str, str]:
    #if max_waiting_time > 0:
    #    time.sleep(random.randint(1 * 100, max_waiting_time * 100) / 100)

    get_my_logger().info(f'Request: Horarios para canje de licencia en {office} para {country}')

    response = get_response(country=country, office=office, retries_sleep_seconds=max_waiting_time)

    lookup_status, msg = get_lookup_status(response=response)

    kr.save_response(filename=f'./var/responses/{suggest_filename(response)}',
                     response=response)

    return lookup_status, msg
