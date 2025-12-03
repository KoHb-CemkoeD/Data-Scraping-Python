from math import nan, sqrt
from time import sleep

from bs4 import BeautifulSoup
import requests
from datetime import datetime
from user_agent import generate_user_agent

# proxies = {'http' : 'https://83.166.226.72:5678',
#           'https': 'https://83.166.226.72:5678'}

headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}

URL = 'https://www.foxtrot.com.ua/uk/shop/mobilnye_telefony_smartfon.html?page='
URL_PREFIX = "https://www.foxtrot.com.ua"

data_dict = {"brand": '', "model": '', "RAM": nan, "ROM": nan, "display_ih": nan, "display_type": '', "display_h": nan,
             "display_w": nan, "ppi": nan, "battery_cap": nan, "mem_card_support": 0,
             "SIM_am": nan, "cpu_cores": nan, "cpu_max_freq": nan, "main_camera_mp": nan,
             "front_camera_mp": nan, "bt_version": nan, "OS": nan, "back_panel": '', "body": '',
             "width": nan, "height": nan, "depth": nan, "weight": nan, "price": nan}


def parse_soup(soup):
    parsed_data = data_dict.copy()
    price = soup.find('div', attrs={'class': 'card-price'}).getText().strip().removesuffix(" ₴").replace(' ', '')
    content = soup.find('div', attrs={'class': 'popup__content'})
    name = content.find('span').getText().strip().removeprefix("Основні характеристики Смартфон ")

    brand = model = ''
    if "Tecno Camon" in name:
        brand = "Tecno Camon"
        name = name.removeprefix("Tecno Camon ")
    elif "LOGIC INSTRUMENT" in name:
        brand = "LOGIC INSTRUMENT"
        name = name.removeprefix("LOGIC INSTRUMENT ")
    else:
        brand = name[:name.find(" ")]
        name = name[name.find(" "):]

    if '/' in name:
        model = name[:name.find("/") - 2].removeprefix(' ')
    else:
        model = name[:name.find("(") - 1]

    parsed_data["brand"] = brand
    parsed_data["model"] = model
    parsed_data["price"] = int(price)

    features = content.find_all('tr')
    for f in features:
        k = f.find('p').getText().strip()
        v = f.find('a').getText().strip()

        if "," in v:
            v = v.split(",")[0]

        elif k == "Вбудована пам’ять, Гб":
            parsed_data["RAM"] = int(v)

        elif k == "Оперативна пам'ять":
            parsed_data["ROM"] = int(v.removesuffix(' Мб'))

        elif k == "Діагональ дисплея":
            parsed_data["display_ih"] = float(v.removesuffix(' "'))

        elif k == "Матриця":
            parsed_data["display_type"] = v

        elif k == "Роздільна здатність":
            v = v.split("x")
            print(v)
            if len(v) == 1:
                v = v[0].split("х")
            parsed_data["display_h"] = v[0]
            parsed_data["display_w"] = v[1]

        elif k == "Пікселів на дюйм":
            parsed_data["ppi"] = int(v)

        elif k == "Акумулятор":
            parsed_data["battery_cap"] = int(v.removesuffix(" мАг"))

        elif k == "Підтримка карт пам'яті":
            parsed_data["mem_card_support"] = 1 if "до" in v else 0

        elif k == "Кількість SIM-карт":
            parsed_data["SIM_am"] = int(v)

        elif k == "Кількість ядер":
            parsed_data["cpu_cores"] = int(v)

        elif k == "Максимальна частота процесора":
            parsed_data["cpu_max_freq"] = float(v.removesuffix(" ГГц"))

        elif k == "Основна камера":
            parsed_data["main_camera_mp"] = float(v.removesuffix(" Мп"))

        elif k == "Фронтальна камера":
            parsed_data["front_camera_mp"] = float(v.removesuffix(" Мп"))

        elif k == "Версія Bluetooth":
            parsed_data["bt_version"] = float(v)

        elif k == "Операційна система":
            parsed_data["OS"] = v[:v.find(' ')]

        elif k == "Матеріал задньої кришки":
            parsed_data["back_panel"] = v

        elif k == "Корпус":
            parsed_data["body"] = v

        elif k == "Розмір":
            v = map(float, v.removesuffix("мм").replace("x", "").replace("х", "").split())
            parsed_data["width"], parsed_data["height"], parsed_data["depth"] = v

        elif k == "Вага":
            parsed_data["weight"] = int(v.removesuffix(" г"))
    return parsed_data


def save_data(data):
    values = [d.values() for d in data]
    data_text = ','.join(data_dict.keys()) + '\n'
    for row in values:
        cur_row_text = ''
        for col in row:
            if isinstance(col, str):
                cur_row_text += ('"' + col + '",')
            else:
                cur_row_text += (str(col) + ',')
        data_text += (cur_row_text.removesuffix(',') + '\n')

    with open("foxtrot.txt", "a", encoding='utf-8') as w:
        w.write(data_text)


def collect_data(links):
    data, i, link = [], 0, ''
    for link in links:
        print(f"\nattempt {i}, getting data..., URL: {link}, time: {datetime.now().time()}", end=" ")
        # try:
        soup = BeautifulSoup(requests.get(link, timeout=10, headers=headers).content, 'html.parser')
        print(", data received. time:", datetime.now().time())

        if not soup:
            continue
        cur_data = parse_soup(soup)

        if cur_data["price"] and cur_data["brand"]:
            data.append(cur_data)

        # except Exception as e:
        #     print(e)
        #     break
        i += 1
        print(f"  success, collected: {i} pages, time: {datetime.now().time()}\n")
        sleep(3)

    print("collected: ", len(data), "attempts:", i, "last page:", link)
    print()

    save_data(data)


def collect_data_links():
    a_list = []
    for i in range(1, 18):
        print("attempt", i + 1, ",", URL + str(i), ", getting data... time:", datetime.now().time(), end=" ")
        try:
            soup = BeautifulSoup(requests.get(URL + str(i), timeout=10, headers=headers).content, 'html.parser')
            print(", data received. time:", datetime.now().time())
            content = soup.find_all('div', attrs={'class': 'card__body'})
            for a in content:
                a_list.append(a.find('a', attrs={'class': 'card__title'}).get_attribute_list("href")[0])
            if not content:
                continue

        except Exception as e:
            print(e)
            break
        print("  success, URL:", URL + str(i), "time:", datetime.now().time(), "\n")
        sleep(3)

    print(a_list)
    data_text = '\n'.join(map(lambda s: URL_PREFIX + s, a_list))
    with open("foxtrot_urls.txt", "w", encoding='utf-8') as w:
        w.write(data_text)


def filter_data():
    new_data = []
    sets = []
    counter = 0
    with open("foxtrot_new.txt", encoding='utf-8') as o:
        data = o.read().split('\n')
    # print("dataset len:", len(data) - 2)
    # print(data[r])
    data_m = data[2:]
    for i, d in enumerate(data_m):

        brand, model, RAM, ROM, display_ih, display_type, display_h, display_w, ppi, battery_cap, mem_card_support, cpu_cores, main_camera_mp, front_camera_mp, bt_version, OS, back_panel, body, price = d.split(
            ',')
        # sets.append(width)
        # if width == 'nan':
        #     counter += 1
        #     print(d)
        if body == '""': body = '"нерозбірний"'
        if bt_version == 'nan': bt_version = '5.0'
        if back_panel == '""': back_panel = '"пластик"'
        if "iPhone SE" in d or "iPhone 12" in d or "iPhone 13" in d: cpu_cores = '6'

        if "iPhone SE" in d: battery_cap = '1821'

        elif "iPhone 12 Pro Max" in d: battery_cap = '3687'
        elif "iPhone 12 Pro" in d: battery_cap = '2815'
        elif "iPhone 12 mini" in d: battery_cap = '2227'
        elif "iPhone 12" in d: battery_cap = '2815'

        elif "iPhone 13 Pro Max" in d: battery_cap = '4352'
        elif "iPhone 13 Pro" in d: battery_cap = '3095'
        elif "iPhone 13 mini" in d: battery_cap = '2406'
        elif "iPhone 13" in d: battery_cap = '3327'

        if ppi == 'nan':
            ppi = str(sqrt((int(display_h.replace('"', '')) ** 2) + (int(display_w.replace('"', '')) ** 2)) // float(display_ih.replace('"', ''))).removesuffix(".0")

        new_data.append(','.join([brand, model, RAM, ROM, display_ih, display_type, display_h, display_w, ppi, battery_cap, mem_card_support, cpu_cores, main_camera_mp, front_camera_mp, bt_version, OS, back_panel, body, price]))

        # cpu_max_freq,, SIM_am
    print("data with rating:", len(new_data))
    print(counter)
    print(sorted(set(sets)))
    # print("data 0:", new_data[777])
    # print("studios:", sorted(list(set(studios))))
    data_text = data[0] + '\n\n'
    for row in new_data:
        data_text += (row + '\n')

    # with open("foxtrot_new.txt", "w", encoding='utf-8') as w:
    #     w.write(data_text)
