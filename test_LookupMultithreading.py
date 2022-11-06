import concurrent
from unittest import TestCase

import Lookup
from LookupMock import mock_request_post_with_random_response
from LookupMultithreading import schedule_lookup, file_to_lines
from MyLogger import get_my_logger
from LookupMultithreading import process_pending


class TestLookupMultithreadingMocked(TestCase):

    def test_lookup_multithreading(self):
        mock_request_post_with_random_response(path='etc/tests/responses/selected')
        schedule_lookup()

    def test_lookup_monothreading(self):
        mock_request_post_with_random_response(path='etc/tests/responses/selected')
        offices = file_to_lines(filename="./etc/reemplazar_licencia/Offices.txt")
        countries = file_to_lines(filename="./etc/reemplazar_licencia/Countries.txt")
        pending_list: list = []
        for office in offices:
            for country in countries:
                pending_list.append([office, country])
        for pending in pending_list:
            process_pending(pending)

