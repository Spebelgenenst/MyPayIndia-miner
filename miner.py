import requests
import time
import json
import argparse

parser = argparse.ArgumentParser(
    prog='MyPayIndia Miner',
    description="A better free lightweight autoclicker for MyPayIndia. Mine MPI inr for free and make money $$$$",
    epilog='made by spebelgenenst website: spebell.com github: github.com/spebelgenenst'
)

parser.add_argument("-m", "--mine", help="start mining", action='store_true')

parser.add_argument("-l", "--list", help="list all acounts and removes invalid session ids", action='store_true')
parser.add_argument("-a", "--add", help="add a new account. write username or session id")
parser.add_argument("-r", "--remove", help="removes an account. write number or session id")

parser.add_argument("-c", "--config", help="select the config file (default: CONFIG_FILE)")
parser.add_argument("-u", "--url", help="select the base url (default: https://mypayindia.com)")

parser.add_argument("-d", "--calibrate", help="(re)calibrate the delay for each request", action='store_true')

args = parser.parse_args()

# If no arguments are provided, show help
if not any(vars(args).values()):
    parser.print_help()
    quit()

BASE_URL = "https://mypayindia.com" if not args.url else args.url

CONFIG_FILE = "config.json" if not args.config else args.config

try:
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

except (FileNotFoundError, json.JSONDecodeError, KeyError):
    config = {"sessionID": [], "sleepTime": ""}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

sleep_time = config["sleepTime"]
session_ids = config["sessionID"]

def mine(csrf_token, session_id):
    headers = {
        "X-CSRF-TOKEN": csrf_token,
        "Authorization": f"Bearer {session_id}"
    }
    url = BASE_URL+"/iotm/button/click"
    return requests.post("https://mypayindia.com/iotm/button/click", headers=headers)


def get_csrf_token(session_id):
    headers = {
        "Authorization": f"Bearer {session_id}"
    }

    response = requests.get("https://mypayindia.com/iotm/button", headers=headers).text

    search = "const csrfToken = \""
    csrf_token_location = response.find(search)

    if csrf_token_location == -1:
        print(response)
        print("csrf token not found")
        quit()

    start = csrf_token_location + len(search)
    csrf_token = response[start:start+40]

    return csrf_token

def login(username):
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
        return False, None

    return True, response.get("data").get("session_id")

def check_session(session_id):
    url=BASE_URL+"/api/v2/user/info"
    headers = {
        "Authorization": f"Bearer {session_id}"
    }

    response = requests.get(url, headers=headers).json()
    if response.get("success"):
        return response.get("data").get("username"), True

    return None, False

def check_users(session_ids):
    output = ""
    accs_removed = 0
    for index, session_id in enumerate(session_ids):
        name, valid = check_session(session_id)
        if valid:
            output += f"\n{index} {name}"
        else:
            config["sessionID"].remove(session_id)
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f)
            session_ids = config["sessionID"]
            accs_removed += 1

    output += f"\ninvalid session ids removed: {accs_removed}"
    return output, session_ids

def check_for_cooldown(csrf_token, session_id):
    # make sure there is no cooldown rn
    response = mine(csrf_token, session_id).json()
    if not response.get("success"):
        print("\"slow down\" cooldown... please wait a sec")
        time.sleep(19)
    time.sleep(1)

def sleep_time_calibration(csrf_token, session_id):
    check_for_cooldown(csrf_token, session_id)

    print("started calibration... (this may take a while (it will take more than 5 mins))")
    clicks_per_second = 1 # (you have to multiply them by 10)
    loss = 0
    tries = 100
    best_successfull_cps = 1 #always the last one

    #calibration (get the best cps)
    while True:
        sleep_time = 1/clicks_per_second

        for i in range(0, tries):
            response = mine(csrf_token, session_id).json()
            if not response.get("success"):
                loss += 1
            time.sleep(sleep_time)

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
    time.sleep(20)

    return sleep_time

if args.list:
    output, session_ids = check_users(session_ids)
    print(output)

if args.add:
    session_id = args.add
    username, success = check_session(args.add) #args.add = session id ?

    if not success:
        username = args.add #username will be used later
        success, session_id = login(username) #args.add = username

        if not success:
            print("credentials wrong!")
            quit()

    session_ids.append(session_id)
    config["sessionID"] = session_ids
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)
    print(f"succesfully added {username}!")

if args.remove:
    if args.remove in session_ids:
        session_ids.remove(args.remove)
    else:
        session_ids.pop(int(args.remove))

    config["sessionID"] = session_ids
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

    


if not (args.calibrate or args.mine):
    quit()

_, session_ids = check_users(session_ids)

if len(session_ids) == 0:
    print("unable to do this action, no user registered! please use -a to add a user")
    quit()
csrf_token = get_csrf_token(session_ids[0])

if not sleep_time or args.calibrate:
    if input("Do you wanna use the default value instead of starting calibration? (Y|n)") != "n":
        sleep_time = 0.6666666666666665
    else:
        sleep_time = sleep_time_calibration(csrf_token, session_ids[0])

    config["sleepTime"] = sleep_time
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

if args.mine:
    # the real magic
    print("mining started....")
    while True:
        start_time = time.time()

        for session_id in session_ids:
            mine(csrf_token, session_id)

        time.sleep(sleep_time - (time.time() - start_time))