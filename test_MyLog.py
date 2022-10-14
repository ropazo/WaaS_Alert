from unittest import TestCase
import MyLogger


class MyException(Exception):
    pass


class TestMyLog(TestCase):

    def test_every_logging_type(self):
        print('Probando mis logs:')
        my_logger = MyLogger.getMyLogger(__name__)
        print(f'Tipo de my_logger: {type(my_logger)}')
        my_logger.debug('DEBUG: Soy un log de debug')
        my_logger.info('INFO: Soy un log de info')
        my_logger.warning('WARNING: Soy un log de warning')
        my_logger.error('ERROR: Soy un log de error')
        my_logger.critical('CRITICAL: Soy un log critical')
        my_logger.debug('Log con caracteres especiales: ñáéíóú')
        # Si se ejecuta lo siguiente, MyLogger funciona bien, pero el test falla.
        # raise MyException
