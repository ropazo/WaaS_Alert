from unittest import TestCase
import Scheduler


class TestLookupMocked(TestCase):

    def test_get_check_point(self):
        office, country = Scheduler.get_check_point()
        print(f'{office} - {country}')

    def test_set_check_point(self):
        office = 'myOffice'
        country = 'myCountry'
        Scheduler.set_check_point(office=office, country=country)
        saved_office, saved_country = Scheduler.get_check_point()
        self.assertEqual(office, saved_office)
        self.assertEqual(country, saved_country)


