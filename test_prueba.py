from unittest import TestCase
from unittest.mock import Mock
import prueba


def my_mocked_function(s) -> int:
    return int(s) + 7


class TestPrueba(TestCase):

    def test_simple_call(self):
        prueba.my_function = Mock()
        prueba.my_function.return_value = 7
        a = prueba.my_function('21')
        print(f'a = {a}')
