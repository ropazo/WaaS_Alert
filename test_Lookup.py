from unittest import TestCase
from unittest.mock import Mock
import Lookup
import json
from KhRequest import log_pretty_response
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
        response = kr.load_response(filename=f'{dir_name}/{filename}')
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


def erase_dots_from_right(s: str) -> str:
    its_a_dot = True
    aux = s
    while its_a_dot:
        if aux[len(aux) - 1] == '.':
            aux = aux[0:len(aux) - 1]
        else:
            its_a_dot = False
    return aux


def get_data_from_filename(filename: str) -> [int, str, str, str, str, str]:
    s1 = '504 timeout.   Barcelona.....................  Costa Rica..   msg=html code...................................................  uid=24211'
    s2 = '01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789'
    s4 = '    00        01        02        03        04        05        06        07        08        09        10        11        12        13    '
    status_code = int(filename[0:3])
    lookup_status = filename[4:4 + 8].replace('.', '')
    office = erase_dots_from_right(filename[15:15 + 30])
    country = erase_dots_from_right(filename[47:47 + 12])
    msg = filename[66:66 + 60]
    uid = filename[132:132 + 6]
    return status_code, lookup_status, office, country, msg, uid


def test_directory(path: str) -> str:
    response_files = [f for f in os.listdir(path) if isfile(join(path, f))]
    for filename in response_files:
        print(filename)
        status_code_1, lookup_status_1, office_1, country_1, msg_1, uid_1 = get_data_from_filename(filename=filename)
        response = kr.load_response(filename=f'{path}/{filename}')
        kr.mock_post(response=response)
        office_2, country_2 = Lookup.get_office_and_country(response)
        lookup_status_2, msg_2 = Lookup.lookup(office=office_1, country=country_1, retries_sleep_seconds=0)
        msg_2 = msg_2.replace('"', '-')
        if lookup_status_1 < lookup_status_2:
            lookup_status_2 = lookup_status_2[0:len(lookup_status_1)]
        else:
            msg_1 = msg_1[0:len(msg_2)]
        if msg_1 < msg_2:
            msg_2 = msg_2[0:len(msg_1)]
        else:
            msg_1 = msg_1[0:len(msg_2)]
        intro = f'Error al validar el siguiente archivo:\n{filename}\n'
        if status_code_1 != response.status_code:
            return f'{intro}status_code: {status_code_1} != {response.status_code}'
        elif lookup_status_1 != lookup_status_2:
            return f'{intro}lookup_status: {lookup_status_1} != {lookup_status_2}'
        elif office_1 != office_2.replace('/', '-'):
            return f'{intro}office: *{office_1}* != *{office_2}*'
        elif country_1 != country_2.replace('/', '-'):
            return f'{intro}country: {country_1} != {country_2}'
        elif msg_1[0:len(msg_2)] != msg_2:
            return f'{intro}msg: {msg_1} != {msg_2}'
    return ''


class TestMocked(TestCase):

    def test_log(self):
        response = kr.load_response(filename='./var/responses/401 last.response')
        log_pretty_response(response=response)

    def test_get_filename(self):
        response = kr.load_response(filename='./var/responses/401 last.response')
        file_name = Lookup.suggest_filename(response)
        print('Nombre sugerido:')
        print(file_name)

    def test_rename_responses_files(self):
        # rename_responses(dir_name='./etc/tests/responses/selected')
        # rename_responses(dir_name='./etc/tests/responses/selected')
        rename_responses(dir_name='./etc/tests/responses/many')
        # rename_responses(dir_name='./var/responses')

    def test_lookup(self):
        response = kr.load_response(filename='./etc/tests/responses/selected/200 ok.response')
        kr.mock_post(response=response)
        office, country = Lookup.get_office_and_country(response)
        lookup_status, msg = Lookup.lookup(office=office, country=country)
        get_my_logger().critical(f'{lookup_status:>10} - {office} - {country} - {msg}')
        self.assertEqual(lookup_status, 'ok')
        self.assertEqual(response.status_code, 200)

    def test_RequestException(self):
        filename = ('./etc/tests/responses/selected/200 ok......   Córdoba.......................  ' \
                    'Brasil......   msg=None........................................................  '
                    'uid=82773.response')
        response = kr.load_response(filename=filename)
        kr.mock_post_with_exception(response=response, mocked_exception=requests.exceptions.RequestException)
        office, country = Lookup.get_office_and_country(response)
        try:
            Lookup.lookup(office=office,
                          country=country,
                          retries_sleep_seconds=0)
        except kr.ErrorNotRecovered:
            pass
        else:
            self.fail('Se esperaba una excepción')

    def test_create_some_responses__no_test(self):
        i_want_to_create_some_responses = False
        if i_want_to_create_some_responses:
            response = Lookup.get_response(office='Alicante/Alacant', country='Alemania')
            file_name: str = './test/response_sample_2.bin'
            kr.save_response(filename=file_name, response=response)
            log_pretty_response(response=response)

    def test_selected_responses(self):
        error = test_directory(path='etc/tests/responses/selected')
        if error != '':
            self.fail(error)

    def test_many_responses(self):
        error = test_directory(path='etc/tests/responses/many')
        if error != '':
            self.fail(error)


class TestLookupReal(TestCase):

    def test_basic_call(self):
        lookup_status, message = Lookup.lookup(office="Valencia/València", country="Chile")
        get_my_logger().critical(f'Respuesta recibida\n\tStatus = {lookup_status}\n\tMensaje = {message}')

    def test_lookup_many_responses(self):
        r_path = 'etc/tests/responses/many'
        response_files = [f for f in os.listdir(r_path) if isfile(join(r_path, f))]
        for file_name in response_files:
            response = kr.load_response(filename=f'{r_path}/{file_name}')
            lookup_status, msg = Lookup.lookup(office="mocked", country="mocked")
            print(f'\n\n{lookup_status} *** {msg}\n')


class TestBasicUnits(TestCase):

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

    def test_erase_dots_from_right(self):
        self.assertEqual('Hola', erase_dots_from_right('Hola....'))
        self.assertEqual('Hola.Chao', erase_dots_from_right('Hola.Chao...'))
        self.assertEqual('Chao', erase_dots_from_right('Chao'))
        self.assertEqual('...Hola.Chao', erase_dots_from_right('...Hola.Chao...'))

    def test_mocked_way(self):
        kr.mock_post()
        kr.post_request_to_test()

    def test_get_data_from_filename(self):
        filename = ('504 timeout.   Barcelona.....................  Costa Rica..   '
                    'msg=html code...................................................  uid=24211')
        status_code, lookup_status, office, country, msg, uid = get_data_from_filename(filename=filename)
        self.assertEqual(504, status_code)
        self.assertEqual('timeout', lookup_status)
        self.assertEqual('Barcelona', office)
        self.assertEqual('Costa Rica', country)
        self.assertEqual('html code...................................................', msg)
        self.assertEqual('24211', uid)
