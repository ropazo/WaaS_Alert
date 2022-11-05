import requests

roberto_opazo_api_key = 'u6ToRHDM5xZmnmXzNpr5ZxUKA5y2Fg'

user_api_key = roberto_opazo_api_key

app_api_key = 'a2s75u6tvhk2u83ao3q6ee2wok2guu'

r = requests.post("https://api.pushover.net/1/messages.json", data={
    "token": app_api_key,
    "user": user_api_key,
    "message": "Ya perdí la cuenta de la cantidad de pruebas"
},
                  )
print(r.text)
