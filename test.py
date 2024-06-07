import json
import requests
import pprint


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


def get_FWI_info(lat, lon):
    url = "https://opendata-download-metfcst.smhi.se/api/category/fwif1g/version/1/daily/parameter.json"
    response = requests.get(url)
    content = get_json_content_from_response(response)
    if content:
        # Sprawdź, czy klucz "fwiindex" jest w danych
        if "fwiindex" in content:
            fwiindex_data = content["fwiindex"]
            for data in fwiindex_data:
                # Tutaj przetwarzaj dane zgodnie z Twoimi potrzebami
                # Możesz wydrukować dane lub zapisywać je do pliku, bazy danych itp.
                pprint.pprint(data)
        else:
            print("No FWI data found in the response")


city_name = "London"
lat, lon = get_lat_and_lon(city_name)  # type: ignore
if lat and lon:
    print("hey")
    get_FWI_info(lat, lon)
