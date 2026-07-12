import requests
from time import sleep
import json

BASE_URL = "https://mypayindia.com"

with open("config.json", "r") as f:
    config = json.load(f)

session_id = config["sessionID"]
sleep_time = config["sleepTime"]

def login():
    username = input("username: ")
    password = input("password: ")
    auth = input("auth (optional): ")
        
    payload = {
        "username": username,
        "password": password,
        "totp_code": auth
    }
    url=BASE_URL+"/api/v2/auth/login"

    response = requests.post(url, json=payload).json()

    return response.get("success"), response.get("data").get("session_id")

def check_session(session_id):
    if session_id:
        return


    url=BASE_URL+"/api/v2/user/info"
    response = requests.get(url).json()
    if not response.get("error") == 1001:
        return

    success, session_id = login()

    if not success:
        print("login data wrong!")
        quit()

    config["sessionID"] = session_id
    with open('config.json', 'w') as f:
        json.dump(config, f)

def check_for_cooldown(headers, url):
    # make sure there is no cooldown rn
    response = requests.get(url, headers=headers).json()
    if not response.get("success"):
        print("\"slow down\" cooldown... please wait a sec")
        sleep(19)
    sleep(1)

def sleep_time_calibration(headers, url):
    check_for_cooldown(headers, url)

    print("started calibration")
    clicks_per_second = 1 # (you have to multiply them by 10)
    loss = 0
    tries = 100
    best_successfull_cps = 1 #always the last one

    #calibration (get the best cps)
    while True:
        sleep_time = 1/clicks_per_second

        for i in range(0, tries):
            response = requests.get(url, headers=headers).json()
            #print(i, response.get("success"))
            if not response.get("success"):
                loss += 1
            sleep(sleep_time)

        successfull_clicks_percent = (tries - loss) / tries
        succesfull_cps = clicks_per_second * successfull_clicks_percent
        print("clicks per second: ", clicks_per_second)
        print("successfull cps: ",succesfull_cps)
        print("-------")
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



check_session(session_id)

headers = {
    "Authorization": f"Bearer {session_id}"
}
url = BASE_URL+"/accountservices/iotm/button/?click"

if not sleep_time:
    sleep_time = sleep_time_calibration(headers, url)

    config["sleepTime"] = sleep_time
    with open('config.json', 'w') as f:
        json.dump(config, f)


# the real magic
while True:
    response = requests.get(url, headers=headers).json()
    #print(response.get("success"))
    sleep(sleep_time)
