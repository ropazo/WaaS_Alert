import requests

url = "https://api.khipu.com/v1/cl/services/dgt.gob.es/appointments/driver-licence/pick-up"
# ulr a escrapear: https://sedeclave.dgt.gob.es/WEB_NCIT_CONSULTA/solicitarCita.faces
headers = {
    "Content-Type": "application/json",
    "x-api-key": "e32d278a-a299-4c0a-8326-b9c8f950fc4f"
}


def lookup_alert(office: str = "Valencia/València", country: str = "Chile"):
    request_data = {
        "RequestData": {
            "Office": office,
            "Country": country,
        },
        # "CallbackUrl": "https://my-api.my-business.com/api/open-data-response"
    }

    response = requests.post(url, json=request_data, headers=headers)

    return response.text


if __name__ == '__main__':
    lookup_alert()
