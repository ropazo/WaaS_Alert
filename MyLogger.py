"""
MyLogger.py

Asegura que logging:
    * Se configure usando MyLogger.config.yaml y no use la configuración default.
    * Cambie sys.excepthook para que todas las excepciones no capturadas sean logeadas.

Forma de uso:
    from MyLogger import get_my_logger
    my_logger = get_my_logger()
    my_logger.debug('Este es un mensaje de debug')
"""
import logging
import logging.config
import yaml
import sys
from time import gmtime
import inspect
import types
from typing import cast
import ntpath

global __first_time_in_MyLogger__


# Para loguear las Excepciones no capturadas:
def my_handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    print('Planeo logear una excepción no controlada')
    my_logger = get_my_logger()
    my_logger.critical('Uncaught exception: ', exc_info=(exc_type, exc_value, exc_traceback))


def init_my_logger():
    global __first_time_in_MyLogger__
    if '__first_time_in_MyLogger__' not in globals():
        __first_time_in_MyLogger__ = True
    if __first_time_in_MyLogger__:
        with open('etc/MyLogger.config.yaml', 'r') as conf:
            config_my_log = yaml.load(conf, Loader=yaml.FullLoader)
        logging.config.dictConfig(config_my_log)
        logging.Formatter.converter = gmtime
        sys.excepthook = my_handle_exception
        __first_time_in_MyLogger__ = False
        get_my_logger().debug('Módulo MyLogger listo para funcionar')


def get_my_logger():
    func_name = cast(types.FrameType, inspect.currentframe()).f_back.f_code.co_name
    file_name = cast(types.FrameType, inspect.currentframe()).f_back.f_code.co_filename
    file_name = ntpath.basename(file_name).replace(".py", "")
    name = f'{file_name}.{func_name}'
    return logging.getLogger(name=name)


init_my_logger()
