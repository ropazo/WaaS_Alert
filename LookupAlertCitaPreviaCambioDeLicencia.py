import requests
import json
from util import indent


url = "https://api.khipu.com/v1/cl/services/dgt.gob.es/appointments/driver-licence/pick-up"
# ulr a escrapear: https://sedeclave.dgt.gob.es/WEB_NCIT_CONSULTA/solicitarCita.faces
headers = {
    "Content-Type": "application/json",
    "x-api-key": "e32d278a-a299-4c0a-8326-b9c8f950fc4f"
}



def lookup_alert(office: str = "Valencia/València", country: str = "Chile"):
    request_data: dict = {
        "RequestData": {
            "Office": office,
            "Country": country,
        },
        "CallbackUrl": "https://ranopazo.pythonanywhere.com/log_any/"
    }

    response = requests.post(url, json=request_data, headers=headers)

    text = (
        f'Petición a {url}\n'
        f'Request:\n'
        f'\tHeaders =\n{indent(dict(response.request.headers))}\n'
        f'\trequest_data =\n{indent(json.loads(response.request.body))}\n\n'
        f'Response:\n'
        f'\tHeaders =\n{indent(dict(response.headers))}\n'
        f'\tresponse_data =\n{indent(response.json())}\n'
    )
    print(text)

    return text


if __name__ == '__main__':
    lookup_alert()
