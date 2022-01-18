from helpers import read_myjson, store_data, read_folder_myjson

# Read all files in "folder=storage" and try to save in SQL
geojson_list = read_folder_myjson()

for geojson in geojson_list:

    data = read_myjson(geojson)
    print(store_data(data))

