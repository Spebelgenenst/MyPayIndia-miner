import requests
import json

session = requests.Session()

session.cookies.set("PHPSESSID", "<your session id here>")

response = session.get("https://mypayindia.com/iotm/button").text

search = "const csrfToken = \""
csrf_token_location = response.find(search)

if csrf_token_location == -1:
    print(response)
    print("csrf token not found")
    quit()

start = csrf_token_location + len(search)
csrf_token = response[start:start+40]

print(csrf_token_location)
print(start)
print(csrf_token)

headers = {
    "X-CSRF-TOKEN": csrf_token,
}
response = session.post("https://mypayindia.com/iotm/button/click", headers=headers).json()

print(response)
print(response.get("success"))