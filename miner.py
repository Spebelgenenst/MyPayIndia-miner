import requests
from time import sleep
import json

BASE_URL = "https://mypayindia.com"

config_file = "config.json"

try:
    with open(config_file, "r") as f:
        config = json.load(f)
    sleep_time = config["sleepTime"]
    session_ids = config["sessionID"]

except (FileNotFoundError, json.JSONDecodeError, KeyError):
    config = {"sessionID": [], "sleepTime": ""}
    with open(config_file, "w") as f:
        json.dump(config, f)

session = requests.Session()

def mine(csrf_token, session):
    headers = {
        "X-CSRF-TOKEN": csrf_token,
    }
    url = BASE_URL+"/iotm/button/click"
    return session.post("https://mypayindia.com/iotm/button/click", headers=headers)


def get_csrf_token(session):
    response = session.get("https://mypayindia.com/iotm/button").text

    search = "const csrfToken = \""
    csrf_token_location = response.find(search)

    if csrf_token_location == -1:
        print(response)
        print("csrf token not found")
        quit()

    start = csrf_token_location + len(search)
    csrf_token = response[start:start+40]

def login():
    username = input("username: ")
    password = input("password: ")
    auth = input("auth (optional): ")
    if not auth:
        auth = "none"
        
    payload = {
        "username": username,
        "password": password,
        "totp_code": auth
    }
    url=BASE_URL+"/api/v2/auth/login"

    response = requests.post(url, json=payload).json()

    if not response.get("success"):
        print("login data may be wrong!")
        quit()

    return response.get("data").get("session_id")

def check_session(session):
    if config["sessionID"]:
        url=BASE_URL+"/api/v2/user/info"

        response = session.get(url).json()
        if not response.get("error") == 1001:
            return

    session_id = login()

    session.cookies.set("PHPSESSID", session_id)

    config["sessionID"] = session_id
    with open('config.json', 'w') as f:
        json.dump(config, f)

def check_for_cooldown(csrf_token, session):
    # make sure there is no cooldown rn
    response = mine(csrf_token, session).json()
    if not response.get("success"):
        print("\"slow down\" cooldown... please wait a sec")
        sleep(19)
    sleep(1)

def sleep_time_calibration(csrf_token, session):
    check_for_cooldown(csrf_token, session)

    print("started calibration... (this may take a while (it will take more than 5 mins))")
    clicks_per_second = 1 # (you have to multiply them by 10)
    loss = 0
    tries = 100
    best_successfull_cps = 1 #always the last one

    #calibration (get the best cps)
    while True:
        sleep_time = 1/clicks_per_second

        for i in range(0, tries):
            response = mine(csrf_token, session).json()
            if not response.get("success"):
                loss += 1
            sleep(sleep_time)

        successfull_clicks_percent = (tries - loss) / tries
        succesfull_cps = clicks_per_second * successfull_clicks_percent
        print("cps: ", clicks_per_second, "successful: ", succesfull_cps)
        if succesfull_cps < best_successfull_cps:
            clicks_per_second -= 0.1
            break

        best_successfull_cps = succesfull_cps

        
        loss = 0
        clicks_per_second += 0.1

    sleep_time = 1/clicks_per_second

    # wait till the couldown is gone
    print("clicks per second: ", clicks_per_second)
    print("successfull cps: ", best_successfull_cps)
    print("\"slow down\" cooldown... please wait a sec")
    sleep(20)

    return sleep_time



check_session(session)

csrf_token = get_csrf_token(session)

if not sleep_time:
    if input("Do you wanna do calibration? (Y|n)") == "n":
        sleep_time = 0.6666666666666665
    else:
        sleep_time = sleep_time_calibration(csrf_token, session)

    config["sleepTime"] = sleep_time
    with open('config.json', 'w') as f:
        json.dump(config, f)



# the real magic
print("mining started....")
while True:
    mine(csrf_token, session)
    sleep(sleep_time)
