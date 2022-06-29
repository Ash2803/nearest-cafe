import json


with open("coffee.json", "r", encoding='CP1251') as my_file:
    file_contents = my_file.read()

cafe = json.loads(file_contents)
print(cafe)

for name in cafe:
    print(name.get('Name'), name.get('geoData: coordinates'))
# for country in capitals:
#   capital = capitals[country]
#   print("столица {} это {}".format(country,capital))
# first_cafe_name = cafe[0]['Name']
# first_cafe_cord = cafe[0]['geoData']['coordinates']
# print(first_cafe_name, *first_cafe_cord

