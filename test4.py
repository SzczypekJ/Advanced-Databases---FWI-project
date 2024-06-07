import requests

url = "https://weatherapi-com.p.rapidapi.com/current.json"

querystring = {"q": "53.1,-0.13"}

headers = {
    "X-RapidAPI-Key": "ca738b8e03msh0038d8d325449fep187deajsn471c247fe107",
    "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
