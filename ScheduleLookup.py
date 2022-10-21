from LookupAlert import lookup_alert
import datetime
import time
from MyLogger import get_my_logger
import re


def print_intro(waiting_time):
    my_logger = get_my_logger()
    my_logger.critical(
        f'Partiendo una ejecución nueva con {waiting_time / 60:.1f} minutos de espera entre búsquedas...')
    print("Programación de LookupAlert")
    print(f'Tiempo de espera = {waiting_time} segundos')
    print(f'({waiting_time / 60:.1f} minutos)\n')


def schedule_lookup():
    my_logger = get_my_logger()
    waiting_time = 60
    print_intro(waiting_time)
    with open("./etc/reemplazar_licencia/Offices.txt", mode="r", encoding="utf-8") as f:
        offices = f.read().splitlines()
    with open("./etc/reemplazar_licencia/Countries.txt", mode="r", encoding="utf-8") as f:
        countries = f.read().splitlines()
    for office in offices:
        for country in countries:
            office_checked = False
            while not office_checked:
                lookup_status, msg = lookup_alert(office=office, country=country)
                my_logger.critical(f'{lookup_status} - {office} - {country} - {msg}')
                if lookup_status == "ok":
                    my_logger.critical(f'*******   HAY HORARIOS DISPONIBLES - VER ARRIBA   *******')
                if lookup_status != "antibot":
                    office_checked = True
                my_logger.info(f'Sleeping {waiting_time} secs')
                time.sleep(waiting_time)


if __name__ == '__main__':
    schedule_lookup()
