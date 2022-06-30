import json


with open("coffee.json", "r", encoding='CP1251') as my_file:
    file_contents = my_file.read()

cafe_data = json.loads(file_contents)
# print(cafe)

for cafe in cafe_data:
    cafe_name = cafe.get('Name')
    latitude = cafe.get('Latitude_WGS84')
    longitude = cafe.get('Longitude_WGS84')
    print(f"{cafe_name}, {latitude}, {longitude}")

