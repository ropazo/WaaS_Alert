import requests

url = "https://api.khipu.com/v1/cl/services/dtg.gob.es/appointments/driver-licence/pick-up"

payload = {
    "RequestData": {
        "Office": "Valencia/València",
        "Country": "Chile"
    },
}
#    "CallbackUrl": "https://my-api.my-business.com/api/open-data-response"


headers = {
    "Content-Type": "application/json",
    "x-api-key": "fc9ee8f0-3a62-337b-b650-dc2799097861"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
data = response.json()
print(data)
