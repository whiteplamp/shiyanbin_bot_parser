import datetime

import requests
import json


def scrapper(year, week):
    url = f"https://mobifitness.ru/api/v8/club/571/schedule.json?year={year}&week={week}"
    data = json.loads(
        requests.get(url, headers={"authorization": "Bearer 8fa933ca654f2c20e0f5696dc29d4db4a3a287ae"}).text
    )
    return data


def dump_to_file(data, i):
    with open(f'../shiyabin_bot/parser_files/schedule_{i}.json', mode='w', encoding='utf-8') as file:
        json.dump(data, file)


def set_time():
    time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    with open('../shiyabin_bot/parser_files/time.txt', mode='w', encoding='utf-8') as file:
        file.write(time)


def main():
    year = datetime.datetime.today().year
    week = datetime.datetime.today().isocalendar()[1]
    try:
        for i in range(6):
            if week + i > 52:
                data = scrapper(year + 1, week + i - 52)
                dump_to_file(data, i)
            else:
                data = scrapper(year, week + i)
                dump_to_file(data, i)
        set_time()
    except requests.exceptions.Timeout:
        print("error in Timeout request")
    except Exception as error:
        print(error)


if __name__ == '__main__':
    main()
