from Lookup import lookup
import ScheduleLookup
from unittest import TestCase
from PrettyResponse import log_pretty_response
import KhRequest
from os import listdir
from os.path import isfile, join
from MyLogger import get_my_logger


response_with_dump = {
    "OperationId": "1ac3c436-c709-478f-b5b4-f3bc84c45f03",
    "Status": "ERROR",
    "Message": "Por favor, inténtalo más tarde",
    "FailureReason": "TASK_DUMPED",
}


class TestLookupMocked(TestCase):

    def test_log_last_response(self):
        response = KhRequest.load_response(file_name='./etc/tests/responses/selected/504 last.response')
        log_pretty_response(response=response)

    def test_lookup_last_response(self):
        response = KhRequest.load_response(file_name='./etc/tests/responses/selected/504 last.response')
        office = '<mocked>'
        country = '<mocked>'
        lookup_status, msg = lookup(office="mocked", country="mocked", mocked_response=response)
        get_my_logger().critical(f'{lookup_status:>10} - {office} - {country} - {msg}')

    def test_log_basic_ok(self):
        response = KhRequest.load_response(file_name='./etc/tests/responses/selected/200 ok.response')
        log_pretty_response(response=response)

    def test_log_basic_error(self):
        response = KhRequest.load_response(file_name='./etc/tests/responses/selected/401 error-api-key.response')
        log_pretty_response(response=response)

    def test_create_some_responses__no_test(self):
        import Lookup
        response = Lookup.get_response(office='Alicante/Alacant', country='Alemania')
        file_name: str = './test/response_sample_2.bin'
        KhRequest.save_response(file_name=file_name, response=response)
        log_pretty_response(response=response)

    def test_log_selected_responses(self):
        r_path = './etc/tests/responses/selected'
        response_files = [f for f in listdir(r_path) if isfile(join(r_path, f))]
        for file_name in response_files:
            response = KhRequest.load_response(file_name=f'{r_path}/{file_name}')
            log_pretty_response(response=response)

    def test_log_many_responses(self):
        r_path = './etc/tests/responses/many'
        response_files = [f for f in listdir(r_path) if isfile(join(r_path, f))]
        for file_name in response_files:
            response = KhRequest.load_response(file_name=f'{r_path}/{file_name}')
            log_pretty_response(response=response)

    def test_lookup_many_responses(self):
        r_path = './etc/tests/responses/many'
        response_files = [f for f in listdir(r_path) if isfile(join(r_path, f))]
        for file_name in response_files:
            response = KhRequest.load_response(file_name=f'{r_path}/{file_name}')
            lookup_status, msg = lookup(office="mocked", country="mocked", mocked_response=response)
            print(f'\n\n{lookup_status} *** {msg}\n')


class TestLookupReal(TestCase):

    def test_basic_call(self):
        status, message = lookup(office="Valencia/València", country="Chile")
        print(f'Respuesta recibida\n\tStatus = {status}\n\tMensaje = {message}')

    def test_schedule_lookup(self):
        ScheduleLookup.schedule_lookup()

    def test_set_check_point(self):
        office = "test Valencia/València"
        country = "test Chile"
        ScheduleLookup.set_check_point(office=office, country=country)

    def test_get_check_point(self):
        office_2 = "test Valencia/València"
        country_2 = "test Chile"
        self.test_set_check_point()
        office_1, country_1 = ScheduleLookup.get_check_point()
        self.assertEqual(office_1, office_2)
        self.assertEqual(country_1, country_2)

