from random import randint
from time import sleep
import urllib

from bs4 import BeautifulSoup
import requests
from datetime import datetime

from math import nan
from user_agent import generate_user_agent
from googletrans import Translator

# proxies = {'http' : 'https://83.166.226.72:5678',
#           'https': 'https://83.166.226.72:5678'}
from DataCollectorHelper import transform_row

headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}

URL = 'https://multiplex.ua/movie/'

data_dict = {"name": '', "genre": '', "duration": nan, "production_country": '', "studio": '',
             "director": '', "main_role": '', "release": nan, "rental_duration": nan,
             "language": '', "age_limit": nan, "rating": nan}


def collect_data():
    print('cur IP address:', requests.get(r'http://jsonip.com').json()['ip'], "\n")
    data = []
    attempts, first_attempt = 4000, 353566

    for i in range(attempts):
        print('\nattempt:', i + 1, ", getting data... time:", datetime.now().time(), end="")
        try:
            soup = BeautifulSoup(requests.get(URL + str(first_attempt + i), timeout=15, headers=headers).content,
                                 'html.parser')
            print(" data received. time:", datetime.now().time(), end="")
            print()
            content = soup.find('ul', attrs={'class': 'movie_credentials'})
            if not content:
                sleep(1)
                continue
            content_key = content.find_all('p', attrs={'class': 'key'})
            content_val = content.find_all(attrs={'class': 'val'})

            cur_data = data_dict.copy()

            for key, val in zip(content_key, content_val):
                k = key.getText().strip().replace('\t', '').replace('\n', '').replace(':', '')
                v = val.getText().strip().replace('\t', '').replace('\n', '').replace(':', '')
                if "," in v:
                    v = v.split(",")[0]

                if k == "Оригінальна назва":
                    if not v:
                        break
                    cur_data["name"] = v

                elif k == "Рейтинг Imdb":
                    if not v:
                        break
                    cur_data["rating"] = float(v)

                elif k == "Режисер":
                    cur_data["director"] = v

                elif k == "Період прокату":
                    start, end = v.split(" - ")
                    rental = datetime.strptime(end, '%d.%m.%Y') - datetime.strptime(start, '%d.%m.%Y')
                    cur_data["rental_duration"] = rental.days

                elif k == "Мова":
                    cur_data["language"] = v

                elif k == "Жанр":
                    cur_data["genre"] = v

                elif k == "Тривалість":
                    cur_data["duration"] = int(v.replace(' хв.', ''))

                elif k == "Виробництво":
                    cur_data["production_country"] = v

                elif k == "Студія":
                    cur_data["studio"] = v

                elif k == "У головних ролях":
                    cur_data["main_role"] = v

                elif k == "Вік":
                    v = v.removeprefix("+").replace('R', '')
                    if "+" in v:
                        cur_data["age_limit"] = int(v[:v.find('+')])
                    elif "Без" in v:
                        cur_data['age_limit'] = int(v[:v.find("Без") - 1])
                    else:
                        cur_data["age_limit"] = int(v)
                elif k == "Рік":
                    cur_data["release"] = int(v)
            if cur_data["name"] and cur_data["rating"] != nan:
                data.append(cur_data)
        except Exception as e:
            print(e)
            continue
        print("success, URL:", URL + str(first_attempt + i), "time:", datetime.now().time(), "\n\n")
        sleep(3)

    print("collected: ", len(data), ", attempts:", i, "last page:", URL + str(first_attempt + i))

    values = [d.values() for d in data]
    # data_text = ','.join(data_dict.keys()) + '\n'
    data_text = "\n"
    for row in values:
        cur_row_text = ''
        for col in row:
            if isinstance(col, str):
                cur_row_text += ('"' + col + '",')
            else:
                cur_row_text += (str(col) + ',')
        data_text += (cur_row_text.removesuffix(',') + '\n')

    with open("multiplex.txt", "a", encoding='utf-8') as w:
        w.write(data_text)


def filter_data():
    new_data = []
    with open("multiplex.txt", encoding='utf-8') as o:
        data = o.read().split('\n')
    with open("multiplex_0.txt", encoding='utf-8') as o_0:
        data_0 = o_0.read().split('\n')
        data_0 = {d.split(',')[0]: d.split(',')[4] for d in data_0[2:]}
    r = randint(0, len(data) - 2)
    # print("dataset len:", len(data) - 2)
    # print(data[r])
    data_m = data[2:]
    for i, d in enumerate(data_m):
        name, genre, studio, country, \
        duration, age_limit, release, \
        rental_duration, rating = d.split(',')

        old_st = data_0[name]
        if old_st != studio:
            print("old:", old_st, "cur:", studio)
            print(d)
            print()
        new_data.append(','.join([name, genre[:2].upper() + genre[2:], studio, country, duration, age_limit, release,
                                  rental_duration, rating]))

    print("data with rating:", len(new_data))
    # print("data 0:", new_data[777])
    # print("studios:", sorted(list(set(studios))))
    data_text = data[0] + '\n\n'
    for row in new_data:
        data_text += (row + '\n')

    # with open("multiplex.txt", "w", encoding='utf-8') as w:
    #     w.write(data_text)
