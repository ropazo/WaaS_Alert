"""
MyLogger.py

Asegura que logging:
    * Configure usando MyLogger.config.yaml y no use la configuración default.
    * Cambie sys.excepthook para que todas las excepciones no capturadas sean logeadas.
"""
import logging.config
import yaml
import sys


# Para logear las Excepciones no capturadas:
def my_handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return


with open('MyLogger.config.yaml', 'r') as conf:
    config_my_log = yaml.load(conf, Loader=yaml.FullLoader)
logging.config.dictConfig(config_my_log)
sys.excepthook = my_handle_exception


def getMyLogger(name: str):
    return logging.getLogger(name=name)

# Borrar: self.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
