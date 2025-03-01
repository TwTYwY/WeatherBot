import telebot
from deep_translator import GoogleTranslator
import requests
import json
from telebot import types

bot = telebot.TeleBot('7898677651:AAELzbgPSPmeK4r-REMiR8do8ESWUuIw9Fc')
API = '4185b42ecb1f6bfa283f923b456889af'
lastMessages = {}

def checkExistanceOfWebsite(link):
    try:
        response = requests.get(link, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Напиши город, в котором хочешь узнать погоду.')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '<u><b>Вот список сущестующих команд:</b></u>\n\n /start - запустить работу бота', parse_mode='html')

@bot.message_handler(content_types=['text'])
def weather(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Температура', callback_data='temp')
    btn2 = types.InlineKeyboardButton('Погода', callback_data='weather')
    btn3 = types.InlineKeyboardButton('Давление',callback_data='pressure')
    btn4 = types.InlineKeyboardButton('Ветер', callback_data='wind')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    lastMessages[message.chat.id] = message.text
    bot.send_message(message.chat.id, f'Что вы хотите узнать про {message.text}?', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callbackMessage(callback):
    city = GoogleTranslator(sourse="ru", target="en").translate(lastMessages[callback.message.chat.id])
    if checkExistanceOfWebsite(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric'):
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
        data = json.loads(res.text)
        if callback.data == 'temp':
            bot.send_message(callback.message.chat.id, f'Температура: {data["main"]["temp"]} градусов по Цельсию \n Ощущается как: {data["main"]["feels_like"]} градусов по Цельсию')
        elif callback.data == 'weather':
            bot.send_message(callback.message.chat.id, f'Погода: {GoogleTranslator(sourse="en", target="ru").translate(data["weather"][0]["main"])} ({GoogleTranslator(sourse="en", target="ru").translate(data["weather"][0]["description"])})')
        elif callback.data == 'pressure':
            bot.send_message(callback.message.chat.id, f'Давление: {data["main"]["pressure"]} гПа')
        elif callback.data == 'wind':
            bot.send_message(callback.message.chat.id, f'Скорость ветра: {data["wind"]["speed"]} м/с')
    else:
        bot.send_message(callback.message.chat.id, 'Такого города я не знаю(')

bot.infinity_polling()