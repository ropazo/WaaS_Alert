import pickle
from requests.models import Response


def save_response(file_name: str, response):
    dir_name = f'./var/responses'
    file_name = f'{dir_name}/{file_name.replace("/", "")}.response'
    with open(file=file_name, mode='wb') as f:
        pickle.dump(file=f, obj=response, protocol=pickle.HIGHEST_PROTOCOL)


def load_response(file_name: str) -> Response:
    with open(file=file_name, mode='rb') as f:
        response = pickle.load(file=f)
    return response
