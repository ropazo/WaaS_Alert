from unittest import TestCase
from logging import getLogger
import MyLogger

MyLogger.start()


class MyExceptionNotHandled(Exception):
    pass


logs_const = [
    {'type': 'DEBUG', 'msg': 'DEBUG: Soy un log de debug'},
    {'type': 'INFO', 'msg': 'INFO: Soy un log de info'},
    {'type': 'WARNING', 'msg': 'WARNING: Soy un log de warning'},
    {'type': 'ERROR', 'msg': 'ERROR: Soy un log de error'},
    {'type': 'CRITICAL', 'msg': 'CRITICAL: Soy un log critical'},
    {'type': 'SPECIAL', 'msg': 'Log con caracteres especiales: ñáéíóú'},
]


def record_events(logs: list):
    my_logger = getLogger(__name__)
    for log in logs:
        case = log['type']
        if case == 'DEBUG':
            my_logger.debug(log['msg'])
        elif case == 'INFO':
            my_logger.info(log['msg'])
        elif case == 'WARNING':
            my_logger.warning(log['msg'])
        elif case == 'ERROR':
            my_logger.error(log['msg'])
        elif case == 'CRITICAL':
            my_logger.critical(log['msg'])
        elif case == 'SPECIAL':
            my_logger.debug(log['msg'])


class TestMyLog(TestCase):

    def test_regular_expressions(self):
        print('Pruebas simples del funcionamiento de las expresiones regulares')
        self.assertRegex('99', '\\d\\d', 'Formato del registro de log')
        self.assertRegex('2022-10-15 Hola', '\\d\\d\\d\\d-\\d\\d-\\d\\d Hola', 'Formato del registro de log')
        self.assertRegex('2022-10-15 Hola', '\\d\\d\\d\\d-\\d\\d-\\d\\d .*', 'Formato del registro de log')
        self.assertRegex('2022-10-15 Hola:Chao', '\\d\\d\\d\\d-\\d\\d-\\d\\d Hola:Chao', 'Formato del registro de log')
        self.assertRegex('2022-10-15 Hola:Chao,¿Qué tal?', '\\d\\d\\d\\d-\\d\\d-\\d\\d Hola:Chao,.*', 'Formato del registro de log')

        """
        print('Borrar lo siguiente...')
        if pattern.match('9x9') is None:
            self.fail(f"String no satisface la expresión regular:\n"
                      f"\tRecord:\n99\n"
                      f"\tPatrón:\n{pattern.pattern}")
        """

    def test_every_logging_type(self):
        print('Probando tipos de mensaje de log')
        record_events(logs=logs_const)
        # Si se ejecuta lo siguiente, MyLogger funciona bien, pero el test falla porque
        # se trata de probar una excepción no manejada y por lo tanto, se lanza una que no está manejada
        # raise MyExceptionNotHandled

    def test_format(self):
        print('Probando formato del log:')
        record_events(logs=logs_const)
        with open('./var/logs/last_execution.log', 'r') as file:
            for i, line in enumerate(file):
                self.assertRegex(
                    line,
                    '\\d\\d\\d\\d-\\d\\d-\\d\\d \\d\\d:\\d\\d:\\d\\d,\\d\\d\\d - .* - .* - line \\d* - '
                )

    def test_many_initializations(self):
        # Relevante porque logging.config.dictConfig deshabilita los loggers existentes
        # La idea es proteger que una doble llamada produzca una des habilitación de los loggers deseados
        print('Probando que siga funcionando con muchas inicializaciones')
        for i in range(100):
            MyLogger.start()
            my_logger = getLogger(__name__)
            my_logger.info(f'Registrando la fila {i}')
        with open('./var/logs/last_execution.log', 'r') as file:
            for count, line in enumerate(file):
                pass
        self.assertEqual(100, count + 1)
