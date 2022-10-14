import requests

url = "http://127.0.0.1:5000/log_any"

headers = {
    "Content-Type": "application/json",
    "x-api-key": "fc9ee8f0-3a62-337b-b650-dc2799097861"
}

my_json = {
    "title": "Este es my_json",
    "my_sub_json": {
        "my_list": ["a", "aba", "c", "caracol", 5, 6, "elemento 7"]
    }
}

response = requests.post(url, json=my_json, headers=headers)

print(response.text)

