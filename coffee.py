import json
import requests
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


print("Где вы находитесь?")
user_place = input()

apikey = '78bd8346-0a41-4d55-b281-59716f2fc48c'  # ваш ключ

print(f'Ваши координаты {fetch_coordinates(apikey, user_place)}')
