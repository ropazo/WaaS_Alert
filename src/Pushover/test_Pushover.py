from unittest import TestCase
import Pushover


class TestPushover(TestCase):

    def test_notify(self):
        Pushover.notify('Soy test_notify en test_Pushover :-)')
