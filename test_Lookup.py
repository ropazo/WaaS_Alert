from unittest import TestCase
from unittest.mock import Mock
import Lookup
import requests

import json
from PrettyResponse import log_pretty_response
import KhRequest as kr
from os import listdir
from os.path import isfile, join
from MyLogger import get_my_logger
from requests.models import Response

response_with_dump = {
    "OperationId": "1ac3c436-c709-478f-b5b4-f3bc84c45f03",
    "Status": "ERROR",
    "Message": "Por favor, inténtalo más tarde",
    "FailureReason": "TASK_DUMPED",
}
retries_sleep_seconds = 1


def get_error_class(response: Response) -> str:
    code = response.status_code
    if code == 500:
        error_type = 'internal'
    elif code == 504:
        error_type = 'timeout'
    elif code == 401:
        error_type = 'auth'
    elif code == 200:
        data: dict = json.loads(response.text)
        if isinstance(data, str):
            print(f'response no es json: {response.text}')
            error_type = 'no json'
        else:
            if "Status" not in data.keys():
                error_type = 'None'
            elif "FailureReason" not in data.keys():
                error_type = 'None'
            else:
                error_type = f"{data['Status']}+{data['FailureReason']}"
    return error_type


class TestLookupMocked(TestCase):

    def test_log_last_response(self):
        response = load_response(file_name='./var/responses/401 last.response')
        log_pretty_response(response=response)

    def test_lookup_last_response(self):
        response = load_response(file_name='./var/responses/401 last.response')
        office = 'mocked_office'
        country = 'mocked_country'
        lookup_status, msg = Lookup.lookup(office=office, country=country, mocked_response=response)
        get_my_logger().critical(f'{lookup_status:>10} - {office} - {country} - {msg}')

    def test_lookup_mocked_response(self):
        response_file_name = './etc/tests/responses/selected/401 auth - authorization failed.response'
        office, country = kr.mock_request_post(file_name=response_file_name)
        lookup_status, msg = Lookup.lookup(office=office, country=country)
        get_my_logger().critical(f'{lookup_status:>10} - {office} - {country} - {msg}')

    def test_mocked_exception_RequestException(self):
        response_file_name = './etc/tests/responses/selected/401 auth - authorization failed.response'
        office, country = kr.mock_exception_RequestException(file_name=response_file_name)
        with self.assertRaises(Lookup.ErrorNotRecovered):
            Lookup.lookup(office=office,
                          country=country,
                          retries_sleep_seconds=retries_sleep_seconds)

    def test_log_basic_ok(self):
        response = kr.load_response(file_name='./etc/tests/responses/selected/200 ok.response')
        log_pretty_response(response=response)

    def test_log_basic_error(self):
        response = kr.load_response(file_name='./etc/tests/responses/selected/401 error-api-key.response')
        log_pretty_response(response=response)

    def test_create_some_responses__no_test(self):
        import Lookup
        response = Lookup.get_response(office='Alicante/Alacant', country='Alemania')
        file_name: str = './test/response_sample_2.bin'
        kr.save_response(file_name=file_name, response=response)
        log_pretty_response(response=response)

    def test_log_selected_responses(self):
        r_path = 'etc/tests/responses/selected'
        response_files = [f for f in listdir(r_path) if isfile(join(r_path, f))]
        for file_name in response_files:
            response = kr.load_response(file_name=f'{r_path}/{file_name}')
            log_pretty_response(response=response)
            print(f'{response.status_code} {get_error_class(response=response)} --> {file_name}')

    def test_log_many_responses(self):
        r_path = 'etc/tests/responses/many'
        response_files = [f for f in listdir(r_path) if isfile(join(r_path, f))]
        for file_name in response_files:
            response = kr.load_response(file_name=f'{r_path}/{file_name}')
            log_pretty_response(response=response)

    def test_lookup_many_responses(self):
        r_path = 'etc/tests/responses/many'
        response_files = [f for f in listdir(r_path) if isfile(join(r_path, f))]
        for file_name in response_files:
            response = kr.load_response(file_name=f'{r_path}/{file_name}')
            lookup_status, msg = Lookup.lookup(office="mocked", country="mocked", mocked_response=response)
            print(f'\n\n{lookup_status} *** {msg}\n')

    def test_mocked_way(self):
        # kr.mock_post_of_request_to_test()
        kr.mock_post_of_request_to_test()
        kr.post_request_to_test()


class TestLookupReal(TestCase):

    def test_basic_call(self):
        status, message = Lookup.lookup(office="Valencia/València", country="Chile")
        print(f'Respuesta recibida\n\tStatus = {status}\n\tMensaje = {message}')
