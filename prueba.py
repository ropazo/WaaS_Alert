
import KhRequest
from os import listdir
from os.path import isfile, join


r_path = './var/responses'
response_files = [f for f in listdir(r_path) if isfile(join(r_path, f))]
for file_name in response_files:
    response = KhRequest.load_response(file_name=f'{r_path}/{file_name}')
    print(f'{response.status_code}')
