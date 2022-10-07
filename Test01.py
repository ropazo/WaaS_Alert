import requests

url = "https://api.khipu.com/v1/cl/services/dgt.gob.es/appointments/driver-licence/pick-up"

request_data = {
    "RequestData": {
        "Office": "Valencia/València",
        "Country": "Chile"
    },
    # "CallbackUrl": "https://my-api.my-business.com/api/open-data-response"
}

headers = {
    "Content-Type": "application/json",
    "x-api-key": "e32d278a-a299-4c0a-8326-b9c8f950fc4f"
}

response = requests.post(url, json=request_data, headers=headers)

data = response.json()
print(data)
