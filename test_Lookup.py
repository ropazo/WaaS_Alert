from unittest import TestCase
from unittest.mock import Mock
import Lookup
import json
from KhRequest import log_pretty_response, load_response
import KhRequest as kr
import os
from os.path import isfile, join
from MyLogger import get_my_logger
import requests
from requests.models import Response
from pathlib import Path

response_with_dump = {
    "OperationId": "1ac3c436-c709-478f-b5b4-f3bc84c45f03",
    "Status": "ERROR",
    "Message": "Por favor, inténtalo más tarde",
    "FailureReason": "TASK_DUMPED",
}
retries_sleep_seconds = 1


def mock_request_post(file_name: str) -> [str, str]:
    response = load_response(file_name=file_name)
    office, country = Lookup.get_office_and_country(response=response)
    requests.post = Mock()
    requests.post.return_value = response
    return office, country


def get_error_class(response: Response) -> str:
    code = response.status_code
    error_type: str
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


def rename_responses(dir_name: str):
    cur_dir = os.getcwd().replace('\\', '/')
    response_files = [f for f in os.listdir(dir_name) if isfile(join(dir_name, f))]
    for filename in response_files:
        response = kr.load_response(file_name=f'{dir_name}/{filename}')
        new_filename = Lookup.suggest_filename(response)
        print(f'{filename} --> {new_filename}')
        src_full_name = Path(f'{dir_name}/{filename}')
        if new_filename[len(new_filename) - 1] == '.':
            new_filename = new_filename[0:len(new_filename) - 2]
        dst_full_name = Path(f'{dir_name}/{new_filename}.response')
        if len(cur_dir) + len(dir_name) + len(new_filename) + 2 > 255:
            print('Bah. Creí que no podía ser más de 255')
        try:
            os.rename(src=src_full_name, dst=dst_full_name)
        except FileExistsError:
            os.remove(dst_full_name)
            os.rename(src=src_full_name, dst=dst_full_name)


class TestMocked(TestCase):

    def test_log(self):
        response = kr.load_response(file_name='./var/responses/401 last.response')
        log_pretty_response(response=response)

    def test_get_filename(self):
        response = kr.load_response(file_name='./var/responses/401 last.response')
        file_name = Lookup.suggest_filename(response)
        print('Nombre sugerido:')
        print(file_name)

    def test_rename_responses_files(self):
        rename_responses(dir_name='./etc/tests/responses/copied')
        # rename_responses(dir_name='./etc/tests/responses/selected')
        # rename_responses(dir_name='./etc/tests/responses/many')
        # rename_responses(dir_name='./var/responses')

    def test_lookup(self):
        response = kr.load_response(file_name='./etc/tests/responses/selected/200 ok.response')
        kr.mock_post(response=response)
        office, country = Lookup.get_office_and_country(response)
        office, country = Lookup.lookup(office=office, country=country)
        lookup_status, msg = Lookup.lookup(office=office, country=country)
        get_my_logger().critical(f'{lookup_status:>10} - {office} - {country} - {msg}')

    def test_RequestException(self):
        response = kr.load_response(file_name='./etc/tests/responses/selected/200 ok.response')
        kr.mock_post_with_exception(response=response, mocked_exception=requests.exceptions.RequestException)
        office, country = Lookup.get_office_and_country(response)
        office, country = Lookup.lookup(office=office, country=country)
        with self.assertRaises(requests.exceptions.RequestException):
            Lookup.lookup(office=office,
                          country=country,
                          retries_sleep_seconds=retries_sleep_seconds)

    def test_create_some_responses__no_test(self):
        response = Lookup.get_response(office='Alicante/Alacant', country='Alemania')
        file_name: str = './test/response_sample_2.bin'
        kr.save_response(filename=file_name, response=response)
        log_pretty_response(response=response)

    def test_log_selected_responses(self):
        r_path = 'etc/tests/responses/selected'
        response_files = [f for f in os.listdir(r_path) if isfile(join(r_path, f))]
        for file_name in response_files:
            response = kr.load_response(file_name=f'{r_path}/{file_name}')
            log_pretty_response(response=response)
            print(f'{response.status_code} {get_error_class(response=response)} --> {file_name}')

    def test_log_many_responses(self):
        r_path = 'etc/tests/responses/many'
        response_files = [f for f in os.listdir(r_path) if isfile(join(r_path, f))]
        for file_name in response_files:
            response = kr.load_response(file_name=f'{r_path}/{file_name}')
            log_pretty_response(response=response)

    def test_mocked_way(self):
        kr.mock_post()
        kr.post_request_to_test()


class TestLookupReal(TestCase):

    def test_basic_call(self):
        lookup_status, message = Lookup.lookup(office="Valencia/València", country="Chile")
        get_my_logger().critical(f'Respuesta recibida\n\tStatus = {lookup_status}\n\tMensaje = {message}')

    def test_lookup_many_responses(self):
        r_path = 'etc/tests/responses/many'
        response_files = [f for f in os.listdir(r_path) if isfile(join(r_path, f))]
        for file_name in response_files:
            response = kr.load_response(file_name=f'{r_path}/{file_name}')
            lookup_status, msg = Lookup.lookup(office="mocked", country="mocked")
            print(f'\n\n{lookup_status} *** {msg}\n')


class TestReallyUnits(TestCase):

    def test_sfix(self):
        for i in range(1, 100):
            for j in range(1, 100):
                c = 'H'
                s1 = f'{c:.<{i}}'
                s2 = kr.sfix(s1, j)
                print(f's1:\n{s1}\ns2\n{s2}')
                if len(s2) != j:
                    print(f's1:\n{s1}\ns2{s2}')
                    self.fail('s1 <> s2')

