from unittest import TestCase
from CitaPreviaClient.settings import Setup


class TestMocked(TestCase):

    def test_create(self):
        setup = Setup(env_name='DEV')
        print(f'setup = {setup}')

