import requests
from datetime import datetime


def get_json(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        # return f"Error: {response.status_code} - {response.text}"
        raise ValueError("Ошибка при полученных данных")
    
    return response.json()


def proccessing(json):
    data: dict = json

    weather_main = data.get('weather')[0].get('main')
    weather_description = data.get('weather')[0].get('description')
    
    main_temp = data.get('main').get('temp')
    main_feels_like = data.get('main').get('feels_like')
    main_pressure = data.get('main').get('pressure')
    main_humidity = data.get('main').get('humidity')
    main_sea_level = data.get('main').get('sea_level') 
    main_grnd_level = data.get('main').get('grnd_level')

    visibility = data.get('visibility')

    wind_speed = data.get('wind').get('speed')
    wind_deg = data.get('wind').get('deg')

    clouds_all = data.get('clouds').get('all')

    city = data.get('name')
    country = data.get('sys').get('country')

    dt = datetime.fromtimestamp(data.get('dt'))

    sys_sunrise = datetime.fromtimestamp(data.get('sys').get('sunrise'))
    sys_sunset = datetime.fromtimestamp(data.get('sys').get('sunset'))

    caption = f"""Погода в городе {city}, {country}:
Описания: {weather_main} ({weather_description})
Температура: {main_temp}°C 
Ощущается как: {main_feels_like}°C
Влажность: {main_humidity}%
Давление: {main_pressure} гПа
Видимость: {visibility} м
Ветер: {wind_speed} м/с, {wind_deg}°
Облачность: {clouds_all}%
Последнее обновление: {dt.strftime('%d.%m.%Y %H:%M')}
Восход солнца: {sys_sunrise.strftime('%d.%m.%Y %H:%M')}
Закат солнца: {sys_sunset.strftime('%d.%m.%Y %H:%M')}
"""

    return caption 


def get_weather_from_city(city: str):
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=1327e58b44062a45b570ed26a0356900&units=metric&lang=ru"

    try:
        json = get_json(URL)
    
    except ValueError as e:
        return str(e)
    
    else:
        caption = proccessing(json)
        return caption

# print(get_weather_from_city('almaty2'))
