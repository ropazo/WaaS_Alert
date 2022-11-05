from unittest import TestCase
import KhRequest as kr


class TestLookupMultiprocessingMocked(TestCase):

    def test_get_check_point(self):
        response_file_name = './etc/tests/responses/selected/200 last.response'

    office, country = Scheduler.get_check_point()
        print(f'{office} - {country}')

