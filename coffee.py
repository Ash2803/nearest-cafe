import json
import os

import folium
import requests
from dotenv import load_dotenv
from flask import Flask
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


def make_list_of_cafes(cafe_data, your_place_coords):
    cafe_list = []
    for cafes in cafe_data:
        cafe_dict = dict()
        cafe_coords = cafes.get('Latitude_WGS84'), cafes.get('Longitude_WGS84')
        distance_to_cafe = distance.distance(your_place_coords, cafe_coords).km
        cafe_dict['title'] = cafes.get('Name')
        cafe_dict['dist'] = distance_to_cafe
        cafe_dict['latitude'] = cafes.get('Latitude_WGS84')
        cafe_dict['longitude'] = cafes.get('Longitude_WGS84')
        cafe_list.append(cafe_dict)
    return cafe_list


def get_nearest_cafe(cafe):
    return cafe['dist']


def hello_world():
    with open('index.html') as file:
        return file.read()


def show_cafes_on_map(your_place_coords, list_of_sorted_cafes):
    map_coords = folium.Map(location=your_place_coords)
    tooltip = "Click me!"
    for cafes in list_of_sorted_cafes:
        cafe_names = cafes['title']
        cafes_on_map = cafes['latitude'], cafes['longitude']
        folium.Marker(cafes_on_map, popup=cafe_names, tooltip=tooltip, icon=folium.Icon(color='green')).add_to(
            map_coords)
    map_coords.save('index.html')


def main():
    load_dotenv()
    with open("coffee.json", "r", encoding='CP1251') as my_file:
        file_contents = my_file.read()
    cafe_data = json.loads(file_contents)
    apikey = os.getenv('YANDEX_GEO_API_KEY')
    your_place = input("Где вы находитесь? ")
    your_place_coords = fetch_coordinates(apikey, your_place)
    listed_cafe = make_list_of_cafes(cafe_data, your_place_coords)
    list_of_sorted_cafes = sorted(listed_cafe, key=get_nearest_cafe)[:5]
    app = Flask(__name__)
    app.add_url_rule('/', 'hello', hello_world)
    app.run('0.0.0.0')


if __name__ == '__main__':
    main()
