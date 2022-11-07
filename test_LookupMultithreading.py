from unittest import TestCase
from MockResponse import mock_request_post_with_random_response
from LookupMultithreading import lookup_multithreading, file_to_lines
from LookupMultithreading import process_pending


class TestLookupMultithreadingMocked(TestCase):

    def test_lookup_multithreading(self):
        mock_request_post_with_random_response()
        offices_filename = "./etc/reemplazar_licencia/All Offices.txt"
        countries_filename = "./etc/reemplazar_licencia/All Countries.txt"
        lookup_multithreading(offices_filename=offices_filename,
                              countries_filename=countries_filename,
                              max_waiting_time=0.01)

    def test_lookup_monothreading(self):
        mock_request_post_with_random_response()
        offices = file_to_lines(filename="./etc/reemplazar_licencia/All Offices.txt")
        countries = file_to_lines(filename="./etc/reemplazar_licencia/All Countries.txt")
        max_waiting_time = 0
        pending_list: list = []
        for office in offices:
            for country in countries:
                pending_list.append([office, country, max_waiting_time])
        for pending in pending_list:
            process_pending(pending)

