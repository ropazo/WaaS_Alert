from MyLogger import get_my_logger
import requests
import json
from util import indent
import datetime
import re

url = "https://api.khipu.com/v1/cl/services/dgt.gob.es/appointments/driver-licence/pick-up"
# ulr a escrapear: https://sedeclave.dgt.gob.es/WEB_NCIT_CONSULTA/solicitarCita.faces
headers = {
    "Content-Type": "application/json",
    "x-api-key": "e32d278a-a299-4c0a-8326-b9c8f950fc4f"
}


class NewMessageInResponse(Exception):
    pass


def log_request(office, country):
    get_my_logger().info(f'Request: Horarios para canje de licencia en {office} para {country}')


def log_response(response):
    try:
        r_json = response.json()
    except (Exception,) as e:
        my_logger = get_my_logger()
        my_logger.critical(f'response no tiene un json válido. Detalles en log de debug')
        my_logger.debug(f'response no tiene un json válido:\n{response.text}')
        raise e
    text = (
        f'Petición a {url}\n'
        f'Request:\n'
        f'\tHeaders =\n{indent(dict(response.request.headers))}\n'
        f'\trequest_data =\n{indent(json.loads(response.request.body))}\n\n'
        f'Response:\n'
        f'\tHeaders =\n{indent(dict(response.headers))}\n'
        f'\tresponse_data =\n{indent(r_json)}\n'
    )
    msg, status = get_response_status(r_json)
    my_logger = get_my_logger()
    my_logger.info(f'Response: {status} - {msg}')
    my_logger.debug(text)


def get_response_status(r_json) -> [str, str]:
    msg = r_json["Message"]
    status = r_json["Status"]
    return msg, status


def response_to_json(response) -> dict:
    try:
        r_json = response.json()
    except (Exception,) as e:
        my_logger = get_my_logger()
        my_logger.critical(f'response no tiene un json válido. Detalles en log de debug')
        my_logger.debug(f'response no tiene un json válido:\n{response.text}')
        raise e
    return r_json


def get_response(country, office):
    request_data: dict = {
        "RequestData": {
            "Office": office,
            "Country": country,
        },
        #         "CallbackUrl": "https://ranopazo.pythonanywhere.com/log_any/"
    }
    response = requests.post(url, json=request_data, headers=headers)
    return response


def lookup_alert(office: str, country: str) -> [str, str]:
    log_request(office=office, country=country)
    init_time = datetime.datetime.utcnow().isoformat()
    response = get_response(country, office)
    end_time = datetime.datetime.utcnow().isoformat()
    log_response(response=response)
    r_json = response_to_json(response=response)
    lookup_status = get_lookup_status(r_json=r_json)
    return lookup_status, r_json["Message"]


def get_lookup_status(r_json) -> str:
    msg = r_json["Message"]
    if r_json["FailureReason"] in ["TASK_DUMPED"]:
        lookup_status = "ok"
    elif re.match("El horario de atención al cliente está completo.*", msg):
        lookup_status = "complete"
    elif re.match("Estamos recibiendo un número muy elevado de accesos.*", msg):
        lookup_status = "antibot"
    elif re.match("El país no existe.*", msg):
        lookup_status = "country_error"
    else:
        raise NewMessageInResponse(msg)
    return lookup_status
