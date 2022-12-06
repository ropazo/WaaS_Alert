from unittest import TestCase
from MyFiles import file_to_lines
from MyRequests import MockRequests
from LookupMultithreading import lookup_multithreading
from LookupMultithreading import process_pending


class TestLookupMultithreadingMocked(TestCase):

    def test_lookup_multithreading(self):
        mocked_requests = MockRequests()
        mocked_requests.mock_post_with_random_response(repository='tests/CitaPreviaClient/responses/selected')

        offices_filename = "etc/CitaPreviaClient/All Offices.txt"
        countries_filename = "etc/CitaPreviaClient/All Countries.txt"
        lookup_multithreading(offices_filename=offices_filename,
                              countries_filename=countries_filename,
                              max_waiting_time=0.01)

    def test_lookup_monothreading(self):
        mocked_requests = MockRequests()
        mocked_requests.mock_post_with_random_response(repository='tests/CitaPreviaClient/responses/selected')

        offices = file_to_lines(filename="etc/CitaPreviaClient/All Offices.txt")
        countries = file_to_lines(filename="etc/CitaPreviaClient/All Countries.txt")
        max_waiting_time = 0
        pending_list: list = []
        for office in offices:
            for country in countries:
                pending_list.append([office, country, max_waiting_time])
        for pending in pending_list:
            process_pending(pending)
