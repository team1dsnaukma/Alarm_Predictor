import json
import requests
from datetime import datetime, timedelta
with open('token.json', 'r') as file:
    data = json.load(file)

TOKEN = data.get('token', None)

utc_time = datetime.utcnow()

def get_weather_next_12_hours(location, current_time, units):
    future_time = current_time + timedelta(days=1)
    current_date = current_time.strftime('%Y-%m-%d')
    future_date = future_time.strftime('%Y-%m-%d')
    url = (f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{current_date}/'
           f'{future_date}')

    params = {
        'key': TOKEN,
        'unitGroup': units,
        'contentType': 'json',
        "include": "hours"
    }
    response = requests.get(url, params=params)
    print(response.json())


get_weather_next_12_hours("Kyiv,Ukraine", utc_time, "metric")





"""units_default = {
        "us": {"temp": "°F", "wind": "miles per hour", "precip": "inches", "visibility": "miles"},
        "metric": {"temp": "°C", "wind": "kms per hour", "precip": "millimeters", "visibility": "kilometrs"},
        "uk": {"temp": "°C", "wind": "miles per hour", "precip": "millimeters", "visibility": "miles"},
        "base": {"temp": "°K", "wind": "meters per second", "precip": "millimeters", "visibility": "kilometrs"},
    }
    result = {
        "requster_name": name,
        "timestamp": utc_time,
        "location": location,
        "date": date,
        "weather":
            {
                "Description": response["days"][0]["description"],
                "Conditions": response["days"][0]["conditions"],
                "Max temeperature": str(response["days"][0]["tempmax"]) + units_default[units]["temp"],
                "Min temeperature": str(response["days"][0]["tempmin"]) + units_default[units]["temp"],
                "Feels like max": str(response["days"][0]["feelslikemax"]) + units_default[units]["temp"],
                "Feels like min": str(response["days"][0]["feelslikemin"]) + units_default[units]["temp"],
                "UV Index": str(response["days"][0]["uvindex"]) + " / 10",
                "Precip amnt": str(response["days"][0]["precip"]) + " " + units_default[units]["precip"],
                "Precipitation Probability": str(response["days"][0]["precipprob"]) + "%",
                "Wind Speed": str(response["days"][0]["windspeed"]) + " " + units_default[units]["wind"],
                "Visibility": str(response["days"][0]["visibility"]) + " " + units_default[units]["visibility"],
                "Humidity": str(response["days"][0]["humidity"]) + "%"
            }
    }

    return result"""