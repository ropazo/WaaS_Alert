import json

request_data = {
    "RequestData": {
        "Office": "office",
        "Country": "country",
    },
    "CallbackUrl": "https://ranopazo.pythonanywhere.com/log_any"
}

print(f'print:\n{request_data}\n')
print(f'print con indent:\n{json.dumps(request_data, indent=4)}')
