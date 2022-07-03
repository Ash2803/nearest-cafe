import json
import requests
from dotenv import load_dotenv
import os
from geopy import distance

with open("coffee.json", "r", encoding='CP1251') as my_file:
    file_contents = my_file.read()

cafe_data = json.loads(file_contents)


# print(cafe)

# for cafe in cafe_data:
#     cafe_name = cafe.get('Name')
#     latitude = cafe.get('Latitude_WGS84')
#     longitude = cafe.get('Longitude_WGS84')
#     print(f"{cafe_name}, {latitude}, {longitude}")


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


load_dotenv()
apikey = os.getenv('YANDEX_GEO_API_KEY')

first_place = input('Введите Пункт А: ')
second_place = input('Введите Пункт B: ')
print(f'Точка А {fetch_coordinates(apikey, first_place)}')
print(f'Точка B {fetch_coordinates(apikey, second_place)}')
print(distance.distance(first_place, second_place).km)
