import random

import MyLogger
from Lookup import lookup
import time
from MyLogger import get_my_logger
import concurrent.futures


class ParamNotFound(Exception):
    pass


def file_to_lines(filename):
    with open(file=filename, mode="r", encoding="utf-8") as f:
        offices = f.read().splitlines()
    return offices


def process_pending(pending: list):
    office = pending[0]
    country = pending[1]
    max_waiting_time = 5
    my_logger = get_my_logger()
    office_country_checked = False
    while not office_country_checked:
        lookup_status, msg = lookup(office=office, country=country)
        my_logger.critical(f'{lookup_status:>10} - {office} - {country} - {msg}')
        if lookup_status == "ok":
            my_logger.critical(f'*******   HAY HORARIOS DISPONIBLES - VER ARRIBA   *******')
        if lookup_status not in ["antibot", "error", "overload", "timeout2"]:
            office_country_checked = True
        if not office_country_checked:
            waiting_time = random.randint(1, max_waiting_time)
            my_logger.info(f'Sleeping {waiting_time} secs')
            time.sleep(waiting_time)


def schedule_lookup():
    offices = file_to_lines(filename="./etc/reemplazar_licencia/Offices.txt")
    countries = file_to_lines(filename="./etc/reemplazar_licencia/Countries.txt")
    pending_list: list = []
    for office in offices:
        for country in countries:
            pending_list.append([office, country])
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(process_pending, pending_list)


def many_lookups():
    for _ in range(20):
        MyLogger.get_my_logger().critical('-----------------------------------------------------')
        MyLogger.get_my_logger().critical('--------------- Nueva consulta masiva ---------------')
        MyLogger.get_my_logger().critical('-----------------------------------------------------')
        schedule_lookup()
        MyLogger.get_my_logger().critical('-----------------------------------------------------')
        MyLogger.get_my_logger().critical('------------- Fin de la consulta masiva -------------')
        MyLogger.get_my_logger().critical('-----------------------------------------------------')
        time.sleep(60*60)


if __name__ == '__main__':
    many_lookups()
