import requests
from MyLogger import get_my_logger


def notify(msg: str):
    roberto_opazo_api_key = 'u6ToRHDM5xZmnmXzNpr5ZxUKA5y2Fg'
    user_api_key = roberto_opazo_api_key
    app_api_key = 'af348bxx22i3y1auuq711fypdj2bk7'

    my_logger = get_my_logger()
    my_logger.info(f'Notificación por pushover: {msg}')

    r = requests.post("https://api.pushover.net/1/messages.json", data={
        "token": app_api_key,
        "user": user_api_key,
        "priority": 2,
        "retry": 30,
        "expire": 10800,
        "sound": "persistent",
        "message": "Prueba de notificación urgente",
    })

