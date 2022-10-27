from PrettyResponse import log_pretty_response
from MyLogger import get_my_logger
import requests
from requests.models import Response
import json
import datetime
import re
import KhRequest

url = "https://api.khipu.com/v1/cl/services/dgt.gob.es/appointments/driver-licence/pick-up"
# ulr a escrapear: https://sedeclave.dgt.gob.es/WEB_NCIT_CONSULTA/solicitarCita.faces
headers = {
    "Content-Type": "application/json",
    "x-api-key": "e32d278a-a299-4c0a-8326-b9c8f950fc4f"
}


class NewMessageInResponse(Exception):
    pass


def log_record(office, country):
    get_my_logger().info(f'Request: Horarios para canje de licencia en {office} para {country}')


def get_response_status(r_json) -> [str, str]:
    msg = r_json["Message"]
    status = r_json["Status"]
    return msg, status


def response_to_json(response: Response) -> dict:
    my_logger = get_my_logger()
    try:
        r_json: dict = json.loads(response.text)
    except json.JSONDecodeError as e:
        if response.status_code == 504:
            r_json = {
                "OperationId": "",
                "Status": "timeout",
                "Message": response.text,
                "FailureReason": "TIMEOUT"
            }
            my_logger.critical('504: Timeout Internal Server Error')
        elif response.status_code == 500:
            r_json = {
                "OperationId": "",
                "Status": "internal",
                "Message": response.text,
                "FailureReason": "INTERNAL"
            }
            my_logger.critical('504: Timeout Internal Server Error')
        else:
            my_logger.critical(f'response no tiene un json válido. Detalles en log de debug')
            my_logger.debug(f'response no tiene un json válido:\n{response.text}')
            raise e
    if isinstance(r_json, str):
        r_json = {
            "Status": "no_status_in_response",
            "Message": r_json
        }
    if "Status" not in r_json.keys():
        r_json["Status"] = "no_status_in_response"
    if "FailureReason" not in r_json.keys():
        r_json["FailureReason"] = "AUTHORIZATION"
    return r_json


def get_response(country, office, mocked_response: Response = None) -> Response:
    request_data: dict = {
        "RequestData": {
            "Office": office,
            "Country": country,
        },
        #         "CallbackUrl": "https://ranopazo.pythonanywhere.com/log_any/"
    }
    init_time = datetime.datetime.now().replace(microsecond=0)
    if mocked_response is None:
        response = requests.post(url, json=request_data, headers=headers)
    else:
        get_my_logger().info('returning mocked response')
        response = mocked_response
    end_time = datetime.datetime.now().replace(microsecond=0)
    delta_t = end_time - init_time
    KhRequest.save_response(file_name=f'{response.status_code} last', response=response)
    log_pretty_response(response=response, delta_t=delta_t)
    return response


def lookup(office: str, country: str, mocked_response=None) -> [str, str]:
    log_record(office=office, country=country)

    response = get_response(country, office, mocked_response=mocked_response)

    r_json = response_to_json(response=response)
    lookup_status = get_lookup_status(r_json=r_json)

    KhRequest.save_response(file_name=f'{response.status_code} {lookup_status} - {office} - {country}', response=response)

    msg = r_json["Message"] if "Message" in r_json.keys() else ""

    return lookup_status, msg


def get_lookup_status(r_json: dict) -> str:
    msg = r_json["Message"] if "Message" in r_json.keys() else ""
    if r_json["FailureReason"] in ["TASK_DUMPED"]:
        lookup_status = "ok"
    elif r_json["FailureReason"] in ["TASK_EXECUTION_ERROR", "AUTHORIZATION"]:
        lookup_status = "error"
    elif r_json["FailureReason"] in ["TIMEOUT"]:
        lookup_status = "timeout"
    elif r_json["FailureReason"] in ["INTERNAL"]:
        lookup_status = "internal"
    elif re.match("El horario de atención al cliente está completo.*", msg):
        lookup_status = "full"
    elif re.match("Estamos recibiendo un número muy elevado de accesos.*", msg):
        lookup_status = "antibot"
    elif re.match("La oficina ingresada no existe.*", msg):
        lookup_status = "office_err"
    elif re.match("El país no existe.*", msg):
        lookup_status = "country_err"
    else:
        raise NewMessageInResponse(msg)
    return lookup_status
