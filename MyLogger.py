"""
MyLogger.py

Asegura que logging:
    * Configure usando MyLogger.config.yaml y no use la configuración default.
    * Cambie sys.excepthook para que todas las excepciones no capturadas sean logeadas.

Forma de uso:
    import MyLogger
    from logging import getLogger
    MyLogger.init()
    ml = getLogger('__name__')
    ml.debug('Este es un mensaje de debug')
"""
import logging.config
import yaml
import sys
from time import gmtime

global __first_time_in_MyLogger__


# Para loguear las Excepciones no capturadas:
def my_handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return


def start():
    global __first_time_in_MyLogger__
    if '__first_time_in_MyLogger__' not in globals():
        __first_time_in_MyLogger__ = True
    if __first_time_in_MyLogger__:
        with open('./etc/MyLogger.config.yaml', 'r') as conf:
            config_my_log = yaml.load(conf, Loader=yaml.FullLoader)
        logging.config.dictConfig(config_my_log)
        logging.Formatter.converter = gmtime
        sys.excepthook = my_handle_exception
        __first_time_in_MyLogger__ = False
