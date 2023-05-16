import telebot
from decouple import config
import requests
import json

KEY = config("KEY")
bot = telebot.TeleBot(token=KEY)
API = config("API")
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Привет, рад тебя видет! Напишите название города')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message,f'Сейчас погода: {temp}°C')
    
    else:
        bot.reply_to(message,f'Город указан не верно!')


bot.polling(non_stop=True)