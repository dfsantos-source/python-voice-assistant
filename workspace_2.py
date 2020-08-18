import geocoder
import requests
import json
from pprint import pprint

myloc = geocoder.ip('me') # get current location based off ip address
lat = myloc.lat
lon = myloc.lng
part = 'hourly, minutely, current'
api_key = "b06fe66f5475080e660b6feb372b1629"
base_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=imperial&exclude={part}&appid={api_key}"

response = requests.get(base_url)

rough_data = response.json()

weather_forecast = rough_data["daily"]

day_to_get = 0 # range from 0-7

i = 0

output = ""

for elem in weather_forecast:
    #print(f"Current Day: {i}")
    #print(elem["clouds"])
    if (i == day_to_get):
        highTemp = elem["temp"]["max"]
        lowTemp = elem["temp"]["min"]
        weather = elem["weather"]
        x = weather[0]
        weather = x["description"]
        output += f"High temp of: {highTemp} degrees, Low temp of: {lowTemp} degrees, Forecast is: {weather}"
        
    i += 1

print(output)
    
