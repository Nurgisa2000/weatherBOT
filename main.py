# fish
# virtualenv venv/
# source venv/bin/activate.fish
# pip install pyTelegramBotAPI
# pip install geopy
# pip freeze > requirements.txt
# touch config.py main.py weather.py
# python3 main.py


import telebot
from telebot import types
from geopy.geocoders import Nominatim
from config import TOKEN
from weather import get_weather_from_city

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        types.KeyboardButton('Показать погоду', request_location=True)
    )
    first_name = message.from_user.first_name

    text= (
        f'Привет! {first_name} бот, который показывает погоду в твоем городе.\n '
        'Для начала работы введи название своего города.'
    )
    bot.send_photo(
        message.chat.id,
        photo=open('image.png', 'rb'),
        caption=text,
        reply_markup=markup
    )

@bot.message_handler(content_types=['text'])
def get_weather(message: types.Message):
    city = message.text.strip().lower()

    if len(city) < 2:
        bot.send_message(
            message.chat.id,
            'Название города должно содержать не менее 2 символов.'
        )
        return

    if len(city.split()) > 1:
        bot.send_message(
            message.chat.id,
            'Название города должно содержать только одно слово.'
        )
        return

    caption = get_weather_from_city(city)

    bot.send_message(
        message.chat.id,
        caption
    )

@bot.message_handler(content_types=['location'])
def get_location(message: types.Message):
    latitude = message.location.latitude
    longitude = message.location.longitude

    geolocator = Nominatim(user_agent="my_geolocator")
    location_geo = geolocator.reverse(f'{latitude}, {longitude}', language='ru', namedetails=True)
    
    if location_geo.address:
        city = str(location_geo.address).split(', ')[-3]
        
        caption = get_weather_from_city(city)

        bot.send_message(
            message.chat.id,
            caption
        )
    else:
        bot.send_message(message.chat.id, 'Не удалось определить адрес')


print('Bot started...')
bot.polling(none_stop=True)