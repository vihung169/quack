import requests
import time
import json
from threading import Thread
import random

data = {}
with open('data.json', 'r') as f:
    data = json.load(f)

ACCESS_TOKEN =  data['state']['token']
list_collect = []
list_duck = []
count_collect_today = 0
max_duck = 0

def get_total_egg():
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,vi;q=0.8",
        "authorization": "Bearer " + ACCESS_TOKEN,
        "if-none-match": 'W/"1a9-I7Onn3jBU9AHo0MlzSY8mMECNvQ"',
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://dd42189ft3pck.cloudfront.net/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    response = requests.get("https://api.quackquack.games/balance/get", headers=headers)
    if response.status_code == 200:
        data = response.json()
        for item in data['data']['data']:
            if item['symbol'] == "EGG":
                print(f"\nTotal eggs: {item['balance']}")

def get_list_reload():
    global list_duck 
    global list_collect 
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,vi;q=0.8",
        "authorization": "Bearer " + ACCESS_TOKEN,
        "if-none-match": 'W/"1218-LZvWPzXbQkzjfWJ5mauEo0z3f9c"',
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://dd42189ft3pck.cloudfront.net/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    response = requests.get("https://api.quackquack.games/nest/list-reload", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        current_ducks = []

        for item in data['data']['duck']:
            current_ducks.append(item['id'])
        # * Compare duck list
        if list_duck:
            list_duck = current_ducks
        else: 
            list_duck = current_ducks
        
        # ** Compare nest list
        nest_list = []
        for item in data['data']['nest']:
            if item['type_egg']:
                nest_data = { 
                    'id': item['id'],
                    'type_egg': item['type_egg'],
                }
                if(item['type_egg'] > 7):
                    print("type: ", item['type_egg'])
                    print("nest: ", item['id'])
                    if(len(list_duck) < max_duck):
                        print("Good egg")
                        # Hatch egg
                        take_egg(item['id'])
                        time.sleep(4)
                        collect_duck(item['id'])
                        # Collect egg
                nest_list.append(nest_data)
        
        if(nest_list != list_collect):
            list_collect = nest_list
        print("-"*10)
        print("Egg ready to collect:", len(list_collect))
        for collect in list_collect:
            print("Collect: ", collect)

        print("-"*100)
    else:
        print("Error: ", response.status_code)
        print("Error: ", response.text)

def collect():
    if  len(list_collect) == 0:
        return
    # egg = {
    #     'id': 1,
    #     'type_egg': 1
    # }
    for egg in list_collect:
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,vi;q=0.8",
            "authorization": "Bearer " + ACCESS_TOKEN,
            "content-type": "application/x-www-form-urlencoded",
            "priority": "u=1, i",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "Referer": "https://dd42189ft3pck.cloudfront.net/",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }

        data = {"nest_id": egg['id']}
        response = requests.post("https://api.quackquack.games/nest/collect", headers=headers, data=data)

        if response.status_code == 200:
            print("Collect success: ", egg)
            lay_egg(egg)

def lay_egg(egg):
    global count_collect_today
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,vi;q=0.8",
        "authorization": "Bearer " + ACCESS_TOKEN,
        "content-type": "application/x-www-form-urlencoded",
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://dd42189ft3pck.cloudfront.net/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }
    for duck in list_duck:
        data = {"nest_id": egg['id'], "duck_id": duck}
        
        response = requests.post("https://api.quackquack.games/nest/lay-egg", headers=headers, data=data)
        if response.status_code == 200:
            print("Lay egg success: ", egg)
            count_collect_today = count_collect_today + 1
            break
        else:
            time.sleep(0.2)

def remove_duck(duck):
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,vi;q=0.8",
        "authorization": "Bearer " + ACCESS_TOKEN,
        "content-type": "application/x-www-form-urlencoded",
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://dd42189ft3pck.cloudfront.net/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    data = {"ducks": [duck]}

    response = requests.post("https://api.quackquack.games/duck/remove", headers=headers, data=data)

    if response.status_code == 200:
        print("Remove duck success: ", duck)
    else:
        print("Remove duck failed: ", duck)
        print("Error: ", response.text)


def collect_duck(egg):
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,vi;q=0.8",
        "authorization": "Bearer " + ACCESS_TOKEN,
        "content-type": "application/x-www-form-urlencoded",
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://dd42189ft3pck.cloudfront.net/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    data = {"nest_id": egg}

    response = requests.post("https://api.quackquack.games/nest/collect-duck", headers=headers, data=data)

    if response.status_code == 200:
        print("Collect duck success: ", egg)
    else:
        print("Collect duck failed: ", egg)
        print("Error: ", response.text)
        time.sleep(0.2)

def take_egg(egg):
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,vi;q=0.8",
        "authorization": "Bearer " + ACCESS_TOKEN,
        "content-type": "application/x-www-form-urlencoded",
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://dd42189ft3pck.cloudfront.net/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    data = {"nest_id": egg}

    response = requests.post("https://api.quackquack.games/nest/hatch", headers=headers, data=data)

    if response.status_code == 200:
        print("Hatch egg success: ", egg)
    else:
        print("Hatch egg failed: ", egg)
        print("Error: ", response.text)


def get_max_duck():
    global max_duck
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,vi;q=0.8",
        "authorization": "Bearer " + ACCESS_TOKEN,
        "content-type": "application/x-www-form-urlencoded",
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://dd42189ft3pck.cloudfront.net/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    response = requests.get("https://api.quackquack.games/nest/max-duck", headers=headers)

    if response.status_code == 200:
        max_duck = response.json()['data']['max_duck']
        print("Max duck: ", max_duck)
    else:
        print("Get max duck failed")

def get_gold_duck_info():
    global time_to_gold_duck
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,vi;q=0.8",
        "authorization": "Bearer " + ACCESS_TOKEN,
        "content-type": "application/x-www-form-urlencoded",
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://dd42189ft3pck.cloudfront.net/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    response = requests.get("https://api.quackquack.games/golden-duck/info", headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['data']['time_to_golden_duck']
    else:
        print("Get gold duck info failed")

def reward_gold_duck():
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,vi;q=0.8",
        "authorization": "Bearer " + ACCESS_TOKEN,
        "content-type": "application/x-www-form-urlencoded",
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://dd42189ft3pck.cloudfront.net/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    response = requests.get("https://api.quackquack.games/golden-duck/reward", headers=headers)

    if response.status_code == 200:
        print("Reward gold duck success")
        data = response.json()
        return data['data']['type']

def claim_gold_duck(type):
    is_success = False 
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,vi;q=0.8",
        "authorization": "Bearer " + ACCESS_TOKEN,
        "content-type": "application/x-www-form-urlencoded",
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://dd42189ft3pck.cloudfront.net/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }
    body = {"type": type}
    response = requests.post("https://api.quackquack.games/golden-duck/claim", headers=headers, data=body)
    print(response.text)
    if response.status_code == 200:
        print("Claim gold duck success")
        is_success = True
    return is_success

def app_main():
    get_list_reload()
    start_time = time.time()
    while True:
        try:
            get_list_reload()
            get_total_egg()
            collect()
            print(f"Time: {round(time.time() - start_time)}s")
            print(f"Collect: {count_collect_today} eggs")
            print(f"Current Duck: {len(list_duck)}")
            get_max_duck()
            time.sleep(random.randrange(2, 10))
        except Exception as e:
            print(e)
            pass

def gold_duck_threading():
    while True:
        try:
            time_to_collect_gold_duck = get_gold_duck_info()
            print("next time to collect gold duck: ", time_to_collect_gold_duck)
            if(time_to_collect_gold_duck == 0):
                type = reward_gold_duck()
                if type > 0:
                    if(claim_gold_duck(type)):
                        print("Claim gold duck success")
                    else:
                        print("Claim gold duck failed")
            else:
                time.sleep(time_to_collect_gold_duck)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    t1 = Thread(target=app_main, name="app_main")
    t2 = Thread(target=gold_duck_threading, name="gold_duck_threading")

    t1.start()
    t2.start()

    while True: 
        time.sleep(10)