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
#your_place = input("Где вы находитесь? ")
#your_place_coords = fetch_coordinates(apikey, your_place)


for cafe in cafe_data:
    cafes = dict()
    cafe_name = cafe.get('Name')
    latitude = cafe.get('Latitude_WGS84')
    longitude = cafe.get('Longitude_WGS84')
    cafes['title'] = cafe_name
    #cafes['distance'] = distance.distance(cafe_name, your_place_coords).km
    cafes['latitude'] = latitude
    cafes['longitude'] = longitude
    pprint(cafes, sort_dicts=False)
