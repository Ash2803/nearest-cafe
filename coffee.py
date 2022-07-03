import json
import os
from pprint import pprint
from geopy import distance
import requests
from dotenv import load_dotenv

with open("coffee.json", "r", encoding='CP1251') as my_file:
    file_contents = my_file.read()

cafe_data = json.loads(file_contents)


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
    return lat, lon


load_dotenv()
apikey = os.getenv('YANDEX_GEO_API_KEY')
your_place = input("Где вы находитесь? ")
your_place_coords = fetch_coordinates(apikey, your_place)

for cafes in cafe_data:
    cafe_dict = dict()
    cafe_coords = cafes.get('Latitude_WGS84'), cafes.get('Longitude_WGS84')
    distance_to_cafe = distance.distance(your_place_coords, cafe_coords).km
    cafe_dict['title'] = cafes.get('Name')
    cafe_dict['dist'] = distance_to_cafe
    cafe_dict['latitude'] = cafes.get('Latitude_WGS84')
    cafe_dict['longitude'] = cafes.get('Longitude_WGS84')
    cafe_list.append(cafe_dict)


if __name__ == '__main__':
    cafe_list = []
