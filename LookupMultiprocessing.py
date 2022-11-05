import MyLogger
from Lookup import lookup
import time
from MyLogger import get_my_logger
import yaml
from multiprocessing import Pool as ProcessPool


class ParamNotFound(Exception):
    pass


def file_to_lines(filename):
    with open(file=filename, mode="r", encoding="utf-8") as f:
        offices = f.read().splitlines()
    return offices


def process_pending(pending: list):
    waiting_time = 5
    my_logger = get_my_logger()
    office_country_checked = False
    while not office_country_checked:
        office = pending[0]
        country = pending[1]
        lookup_status, msg = lookup(office=office, country=country)
        my_logger.critical(f'{lookup_status:>10} - {office} - {country} - {msg}')
        if lookup_status == "ok":
            my_logger.critical(f'*******   HAY HORARIOS DISPONIBLES - VER ARRIBA   *******')
        if lookup_status not in ["antibot", "error"]:
            office_country_checked = True
        my_logger.info(f'Sleeping {waiting_time} secs')
        time.sleep(waiting_time)


def schedule_lookup():
    my_logger = get_my_logger()
    waiting_time = 10
    offices = file_to_lines(filename="./etc/reemplazar_licencia/Offices.txt")
    countries = file_to_lines(filename="./etc/reemplazar_licencia/Countries.txt")
    pending_list: list = []
    for office in offices:
        for country in countries:
            pending_list.append([office, country])
    with ProcessPool(processes=8) as pool:
        results = pool.map(process_pending, pending_list)


def many_lookups():
    for _ in range(20):
        # set_check_point(office='*****', country='******')
        MyLogger.get_my_logger().critical('-----------------------------------------------------')
        MyLogger.get_my_logger().critical('--------------- Nueva consulta masiva ---------------')
        MyLogger.get_my_logger().critical('-----------------------------------------------------')
        schedule_lookup()
        time.sleep(60*25)


if __name__ == '__main__':
    many_lookups()
