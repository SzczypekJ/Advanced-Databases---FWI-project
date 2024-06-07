import json
import requests
from datetime import datetime


def get_json_content_from_response(response):
    try:
        content = response.json()
    except json.decoder.JSONDecodeError:
        print("Invalid format", response.text)
    else:
        return content


def get_lat_and_lon(city_name):
    params = {
        "q": f"{city_name}",
        "appid": "9a91c2ffcf1f30ac084c7d689b11775a"
    }
    r = requests.get("http://api.openweathermap.org/geo/1.0/direct?", params)
    content = get_json_content_from_response(r)
    if content:
        if len(content) > 0:
            lat = content[0]["lat"]
            lon = content[0]["lon"]
            return lat, lon
        else:
            print("There is no a city with that name")
    else:
        print("No answer from the server")


def get_solar_info(lat, lon, date):
    params = {
        "lat": f"{lat}",
        "lon": f"{lon}",
        "date": f"{date}",
        "appid": "9f93800642c7c2b25b9715cf39d99d24"
    }

    r = requests.get(
        "https://api.openweathermap.org/energy/1.0/solar/data?", params)
    content = get_json_content_from_response(r)
    print('content: ', content)
    if content:
        coord = content.get("coord", {})
        print('coord: ', coord)
        lat = coord.get("lat", "")
        print('lat: ', lat)
        lon = coord.get("lon", "")
        print('lon: ', lon)


city_name = "London"
lat, lon = get_lat_and_lon(city_name)  # type: ignore
print('lat, lon: ', lat, lon)
today = datetime.today().date()
if lat and lon:
    print("hey")
    get_solar_info(lat, lon, today)
