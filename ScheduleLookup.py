from LookupAlertCitaPreviaCambioDeLicencia import lookup_alert
import datetime
import time
office: str = "Valencia/València"
country: str = "Chile"


def schedule_lookup():
    waiting_time = 600
    print("Programación de LookupAlert")
    print(f'Tiempo de espera = {waiting_time} segundos')
    print(f'({waiting_time / 60} minutos)\n')
    while True:
        init_time = datetime.datetime.utcnow().isoformat()
        print(f'{init_time}: Request - horarios para cambio de licencia en {office} para {country}')
        text = lookup_alert()
        end_time = datetime.datetime.utcnow().isoformat()
        print(f'{end_time}: Response - {text}')
        time.sleep(waiting_time)


if __name__ == '__main__':
    schedule_lookup()
