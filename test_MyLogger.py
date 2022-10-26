from unittest import TestCase
from MyLogger import get_my_logger
import threading

logs_const = [
    {'type': 'DEBUG', 'msg': 'Soy un log de debug'},
    {'type': 'INFO', 'msg': 'Soy un log de info'},
    {'type': 'WARNING', 'msg': 'Soy un log de warning'},
    {'type': 'ERROR', 'msg': 'Soy un log de error'},
    {'type': 'CRITICAL', 'msg': 'Soy un log critical'},
    {'type': 'SPECIAL', 'msg': 'Log con caracteres especiales: ñáéíóú'},
]


def record_events(logs: list):
    my_logger = get_my_logger()
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


class TestMyLogBasics(TestCase):
    # No es compatible con TestMyLog porque altera el formato de algunos registros de log

    def test_basic_call(self):
        print('\nPrueba 1')
        my_logger = get_my_logger()
        print(f'1.- my_logger.name = {my_logger.name}')
        get_my_logger().info('Prueba 2')
        print('\nPrueba 2')
        print(f'2.- my_logger.name = {my_logger.name}')
        my_logger.info('Prueba 2\nlinea 2\nlinea 3\nlinea 4\nlinea 5\n')

    def test_regular_expressions(self):
        print('Pruebas simples del funcionamiento de las expresiones regulares')
        self.assertRegex('99', '\\d\\d', 'Formato del registro de log')
        self.assertRegex('2022-10-15 Hola', '\\d\\d\\d\\d-\\d\\d-\\d\\d Hola', 'Formato del registro de log')
        self.assertRegex('2022-10-15 Hola', '\\d\\d\\d\\d-\\d\\d-\\d\\d .*', 'Formato del registro de log')
        self.assertRegex('2022-10-15 Hola:Chao', '\\d\\d\\d\\d-\\d\\d-\\d\\d Hola:Chao', 'Formato del registro de log')
        self.assertRegex('2022-10-15 Hola:Chao,¿Qué tal?', '\\d\\d\\d\\d-\\d\\d-\\d\\d Hola:Chao,.*',
                         'Formato del registro de log')

        """
        print('Borrar lo siguiente...')
        if pattern.match('9x9') is None:
            self.fail(f"String no satisface la expresión regular:\n"
                      f"\tRecord:\n99\n"
                      f"\tPatrón:\n{pattern.pattern}")
        """


class TestMyLog(TestCase):

    def test_every_logging_type(self):
        print('Probando tipos de mensaje de log')
        record_events(logs=logs_const)

    def test_exception_not_handled(self):
        print(
            """
            No se puede hacer pruebas unitarias de excepciones no controladas porque el módulo unittest
            captura las excepciones no controladas y por lo tanto, no hay excepciones no controladas.
            El código de esta prueba unitaria debe ser copiado a un archivo python que no use unittest. 
            
                from MyLogger import get_my_logger
                
                
                class MyExceptionNotHandled(Exception):
                    pass
                
                
                get_my_logger().info('Validar que en el archivo de log haya quedado registrada'
                                     ' la siguiente excepción: MyExceptionNotHandled')
                raise MyExceptionNotHandled            
            """
        )

    def val_msg_format(self, file_name, line_format):
        print(f'\nValidando el formato en {file_name}')
        with open(file_name, 'r', encoding="utf-8") as file:
            for i, line in enumerate(file.read().splitlines()):
                print(f'***{line}***')
                self.assertRegex(
                    line,
                    line_format
                )

    def test_format(self):
        print('Probando formato del log:')
        record_events(logs=logs_const)
        self.val_msg_format(
            file_name='./var/logs/last_debug.log',
            line_format='\\d\\d\\d\\d-\\d\\d-\\d\\d \\d\\d:\\d\\d:\\d\\d,\\d\\d\\d .* - .* - line \\d*')
        self.val_msg_format(
            file_name='./var/logs/last_critical.log',
            line_format='\\d\\d\\d\\d\.\\d\\d\.\\d\\d \\d\\d:\\d\\d:\\d\\d - Soy un.*')


class TestMyLogConcurrency(TestCase):
    """
    No es compatible con TestMyLog porque la prueba de concurrencia requiere saber la cantidad
    de registros que serán generados.
    """

    def test_many_initializations(self):
        # Relevante porque logging.config.dictConfig deshabilita los loggers existentes
        # La idea es proteger que una doble llamada produzca una des habilitación de los loggers deseados
        print('Probando que siga funcionando con muchas inicializaciones')
        for i in range(100):
            my_logger = get_my_logger()
            my_logger.info(f'Registrando la fila {i}')
        with open('./var/logs/last_info.log', 'r') as file:
            for count, line in enumerate(file):
                pass
        self.assertEqual(100, count + 1)
