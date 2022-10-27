import MyLogger
from Lookup import lookup
import time
from MyLogger import get_my_logger
import yaml


class ParamNotFound(Exception):
    pass


def print_intro(waiting_time):
    my_logger = get_my_logger()
    my_logger.critical(
        f'Partiendo una ejecución nueva con {waiting_time / 60:.1f} minutos de espera entre búsquedas...')
    print("Programación de LookupAlert")
    print(f'Tiempo de espera = {waiting_time} segundos')
    print(f'({waiting_time / 60:.1f} minutos)\n')


def set_check_point(office, country):
    check_point = {
        "office": office,
        "country": country,
    }
    with open("./var/check_point.yaml", mode="w", encoding="utf-8") as f:
        yaml.dump(data=check_point, stream=f, default_flow_style=False, allow_unicode=True)


def get_check_point() -> [str, str]:
    with open("./var/check_point.yaml", mode="r", encoding="utf-8") as f:
        check_point = yaml.safe_load(f)
    office = check_point["office"]
    country = check_point["country"]
    return office, country


def schedule_lookup():
    my_logger = get_my_logger()
    waiting_time = 10
    print_intro(waiting_time)
    with open("./etc/reemplazar_licencia/Offices.txt", mode="r", encoding="utf-8") as f:
        offices = f.read().splitlines()
    with open("./etc/reemplazar_licencia/Countries.txt", mode="r", encoding="utf-8") as f:
        countries = f.read().splitlines()
    # countries = ['Chile']
    cp_office, cp_country = get_check_point()
    if cp_office not in offices or cp_country not in countries:
        at_check_point = True
    else:
        at_check_point = False
    for office in offices:
        for country in countries:
            if not at_check_point:
                if cp_office == office and cp_country == country:
                    at_check_point = True
                else:
                    my_logger.info(f'Jumping {office} {country}, searching checkpoint {cp_office} {cp_country} ')
            else:
                office_country_checked = False
                while not office_country_checked:
                    lookup_status, msg = lookup(office=office, country=country)
                    my_logger.critical(f'{lookup_status:>10} - {office} - {country} - {msg}')
                    if lookup_status == "ok":
                        my_logger.critical(f'*******   HAY HORARIOS DISPONIBLES - VER ARRIBA   *******')
                    if lookup_status not in ["antibot", "error"]:
                        office_country_checked = True
                    my_logger.info(f'Sleeping {waiting_time} secs')
                    time.sleep(waiting_time)
                set_check_point(office=office, country=country)
    set_check_point(office="*** ended ***", country="*** ended ***")


def many_lookups():
    for _ in range(20):
        # set_check_point(office='*****', country='******')
        MyLogger.get_my_logger().critical('-----------------------------------------------')
        MyLogger.get_my_logger().critical('--------------- Nueva ejecución ---------------')
        MyLogger.get_my_logger().critical('-----------------------------------------------')
        schedule_lookup()
        time.sleep(60*25/2)


if __name__ == '__main__':
    many_lookups()
