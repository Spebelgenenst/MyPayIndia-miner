import requests
import json

session = requests.Session()

session.cookies.set("PHPSESSID", "*****")

headers = {
    "X-CSRF-TOKEN": "***",
}
response = session.post("https://mypayindia.com/iotm/button/click", headers=headers).json()

print(response.get("success"))