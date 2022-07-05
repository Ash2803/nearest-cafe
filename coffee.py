import json
import os
from pprint import pprint

import folium
import requests
from dotenv import load_dotenv
from geopy import distance


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


def list_of_cafes():
    for cafes in cafe_data:
        cafe_dict = dict()
        cafe_coords = cafes.get('Latitude_WGS84'), cafes.get('Longitude_WGS84')
        distance_to_cafe = distance.distance(your_place_coords, cafe_coords).km
        cafe_dict['title'] = cafes.get('Name')
        cafe_dict['dist'] = distance_to_cafe
        cafe_dict['latitude'] = cafes.get('Latitude_WGS84')
        cafe_dict['longitude'] = cafes.get('Longitude_WGS84')
        cafe_list.append(cafe_dict)


def get_nearest_cafe(cafe):
    return cafe['dist']


if __name__ == '__main__':
    load_dotenv()
    with open("coffee.json", "r", encoding='CP1251') as my_file:
        file_contents = my_file.read()
    cafe_data = json.loads(file_contents)
    apikey = os.getenv('YANDEX_GEO_API_KEY')
    your_place = input("Где вы находитесь? ")
    your_place_coords = fetch_coordinates(apikey, your_place)
    cafe_list = []
    list_of_cafes()
    list_of_sorted_cafes = sorted(cafe_list, key=get_nearest_cafe)[:5]
    map_coords = folium.Map(location=your_place_coords)
    for cafes in list_of_sorted_cafes:
        cafes_on_map = cafes['latitude'], cafes['longitude']
        folium.Marker([*cafes_on_map], icon=folium.Icon(color='green')).add_to(map_coords)
    map_coords.save('index.html')
