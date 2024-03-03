import json
import requests
import pandas as pd
from datetime import datetime, timedelta
with open('token.json', 'r') as file:
    data = json.load(file)

TOKEN = data.get('token', None)

utc_time = datetime.utcnow()

def get_weather_next_12_hours(location, current_time):
    future_time = current_time + timedelta(days=1)
    current_date = current_time.strftime('%Y-%m-%d')
    future_date = future_time.strftime('%Y-%m-%d')
    url = (f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{current_date}/'
           f'{future_date}')
    params = {
        'key': TOKEN,
        'unitGroup': "metric",
        'contentType': 'json',
        "include": "hours"
    }
    response = requests.get(url, params=params)
    response = response.json()

    weather_by_hour = []
    global_info = [response[info] for info in response if info != "days" and info != "queryCost"]
    column_city = ["city_" + str(info) for info in response if info != "days" and info != "queryCost"]
    for day in response["days"]:
        template = [str(day[info]) for info in day if info != "hours"]
        columns_days = ["day_" + info for info in day if info != "hours"]
        for hour in day["hours"]:
            hour_info = [str(hour[info]) for info in hour]
            columns_hour = ["hour_" + str(info) for info in hour]
            full_info_hour = global_info + template + hour_info
            weather_by_hour.append(full_info_hour)
    rounded_time = current_time.replace(second=0, microsecond=0, minute=0) + timedelta(
        hours=round(current_time.minute / 60))
    formatted_time = rounded_time.strftime('%H:%M:%S')
    weather_current_hour = next((item for item in weather_by_hour if item[42] == formatted_time), None)
    index_current = weather_by_hour.index(weather_current_hour)
    forecast_next_12_hours = weather_by_hour[index_current+1:][:12]
    columns = column_city + columns_days + columns_hour
    forecast_next_12_hours.insert(0, columns)
    df = pd.DataFrame(forecast_next_12_hours[1:], columns=forecast_next_12_hours[0])
    formatted_time = rounded_time.strftime('%H-%M')
    df.to_csv(f"../clean_data/forecast_next_12_hours_from_{current_date} {formatted_time}.csv")



if __name__ == "__main__":
    get_weather_next_12_hours("Kyiv,Ukraine", utc_time)


