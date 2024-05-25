import requests
import time
import json
import sys

data = {}
with open('data.json', 'r') as f:
    # Đọc dữ liệu từ tệp
    data = json.load(f)

ACCESS_TOKEN =  data['state']['token']
list_collect = []
list_duck = []
count_collect_today = 0
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
                    print("Good egg")
                nest_list.append(nest_data)
        
        if(nest_list != list_collect):
            list_collect = nest_list
        print("-"*100)
        print("So trung co the thu thap:", len(list_collect))
        for collect in list_collect:
            print("Collect: ", collect['id'])
            print("Egg Type: ", collect['type_egg'])

            # TODO
            # ! Collect duck
            # 
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
        time.sleep(0.2)


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

    response = requests.post("https://api.quackquack.games/duck/collect", headers=headers, data=data)

    if response.status_code == 200:
        print("Collect duck success: ", egg)
    else:
        print("Collect duck failed: ", egg)
        print("Error: ", response.text)
        time.sleep(0.2)

get_list_reload()
start_time = time.time()
while True:
    get_list_reload()
    get_total_egg()
    collect()
    print(f"Time: {round(time.time() - start_time)}s")
    print(f"Collect: {count_collect_today} eggs")
    time.sleep(2)