import random
import Pushover
import MyFiles

from Lookup import lookup
import time
from MyLogger import get_my_logger
import concurrent.futures


class ParamNotFound(Exception):
    pass


def process_pending(pending: list):
    office = pending[0]
    country = pending[1]
    max_waiting_time = pending[2] if len(pending) > 2 else 10
    my_logger = get_my_logger()
    office_country_checked = False
    while not office_country_checked:
        lookup_status, msg = lookup(office=office, country=country, max_waiting_time=max_waiting_time)
        my_logger.critical(f'{lookup_status:>10} - {office} - {country} - {msg}')
        # Borrar las siguientes 3 líneas:
        tmp = f'{lookup_status} - {office} - {country}'
        print('*'*(len(tmp)+2*2))
        print(f'* {tmp} *')
        print('*'*(len(tmp)+2*2))
        if lookup_status == "ok":
            my_logger.critical(f'************************************************************************')
            msg = f'*** En {office} hay horarios disponibles para canje de licencia de {country} ***'
            my_logger.critical(msg)
            Pushover.notify(msg=msg)
            my_logger.critical(f'************************************************************************')
        if lookup_status not in ["antibot", "error", "overload", "timeout2"]:
            office_country_checked = True
        if not office_country_checked:
            waiting_time = random.randint(1*100, max_waiting_time*100)/100 if max_waiting_time > 0 else 0
            my_logger.info(f'Sleeping {waiting_time} secs')
            time.sleep(waiting_time)


def lookup_multithreading(offices_filename: str, countries_filename, max_waiting_time: float):
    offices = MyFiles.file_to_lines(offices_filename)
    countries = MyFiles.file_to_lines(countries_filename)
    pending_list: list = []
    for office in offices:
        for country in countries:
            pending_list.append([office, country, max_waiting_time])
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(process_pending, pending_list)


def many_lookups():
    offices_filename = "etc/reemplazar_licencia/Offices.txt"
    countries_filename = "etc/reemplazar_licencia/Countries.txt"
    my_logger = get_my_logger()
    while True:
        """
        my_logger.critical('-----------------------------------------------------')
        my_logger.critical('--------------- Nueva consulta masiva ---------------')
        my_logger.critical('-----------------------------------------------------')
        """
        lookup_multithreading(offices_filename=offices_filename,
                              countries_filename=countries_filename,
                              max_waiting_time=10)
        """
        my_logger.critical('-----------------------------------------------------')
        my_logger.critical('------------- Fin de la consulta masiva -------------')
        my_logger.critical('-----------------------------------------------------\n')
        """
        time_to_sleep = 60*1+(random.randint(1*100, 10*100)/100)
        my_logger.info(f'sleeping {time_to_sleep} secs ({time_to_sleep/60:.1f} mins)...')
        time.sleep(time_to_sleep)


if __name__ == '__main__':
    many_lookups()
