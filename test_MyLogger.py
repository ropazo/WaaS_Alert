from unittest import TestCase
from logging import getLogger
import MyLogger

MyLogger.start()


class MyException(Exception):
    pass


class TestMyLog(TestCase):

    def test_every_logging_type(self):
        print('Probando mis logs:')
        my_logger = getLogger(__name__)
        print(f'Tipo de my_logger: {type(my_logger)}')
        my_logger.debug('DEBUG: Soy un log de debug')
        my_logger.info('INFO: Soy un log de info')
        my_logger.warning('WARNING: Soy un log de warning')
        my_logger.error('ERROR: Soy un log de error')
        my_logger.critical('CRITICAL: Soy un log critical')
        my_logger.debug('Log con caracteres especiales: ñáéíóú')
        # Si se ejecuta lo siguiente, MyLogger funciona bien, pero el test falla.
        # raise MyException

    def test_many_initializations(self):
        # Relevante porque logging.config.dictConfig deshabilita los logs existentes
        print('Probando que siga funcionando con muchas inicializaciones')
        for i in range(100):
            MyLogger.start()
            my_logger = getLogger(__name__)
            my_logger.info(f'Registrando la fila {i}')
        with open('./var/logs/last_execution.log', 'r') as file:
            for count, line in enumerate(file):
                pass
        self.assertEqual(100, count + 1)
