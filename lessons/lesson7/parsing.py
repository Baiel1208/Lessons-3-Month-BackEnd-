# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from dotenv import load_dotenv
# from bs4 import BeautifulSoup
# import os, logging, requests

# from keys import button ,me_sum

# load_dotenv('.env')


# bot = Bot(os.environ.get('token'))
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)
# logging.basicConfig(level=logging.INFO)

# @dp.message_handler(commands='start')
# async def start(message:types.Message):
#     await message.reply(f"""Привет {message.from_user.first_name}! """, reply_markup=button)

# @dp.callback_query_handler(lambda call : call)
# async def inline(call):
#     if call.data == 'USD':
#         await usd(call.message)
#     # elif call.data == 'mesto':
#     #     await pikitochenye(call.message)
#     # elif call.data == 'eda':
#     #     await vkusnozaybal(call.message)
# @dp.message_handler(commands='USD')
# async def usd(message:types.Message):
#     url = 'https://www.nbkr.kg/index.jsp?lang=RUS'
#     responce =requests.get(url)
#     soup=BeautifulSoup(responce.text, 'lxml')
#     currency = soup.find_all('td', class_='exrate')
#     for usd in currency[0:1]:
#         usd_currency = usd.text
#     await message.answer(f"""Вот текущие данные:
# USD:{usd_currency}
# Хотите ввести собственную сумму? нажмите на ==1== если не хотите нажмите на ==2==
# """) 

# @dp.message_handler(text=[1,2,3,4,5])
# async def kazah(message:types.Message):
#     if message.text == '1':
#         await message.answer("Введите собствунную сумму:")
        


# executor.start_polling(dp, skip_updates=True)

import requests
from lxml import etree as et

url = "https://www.nbkr.kg/XML/daily.xml"


def get_curr(currency):
    try:
        quotes = requests.get(url)
    except Exception as e:
        print(e)
        return False
    if quotes.status_code == 200:
        root = et.fromstring(quotes.text.encode('utf-8'))
        for i in root:
            if i.attrib['ISOCode'] == currency:
                for x in i:
                    if x.tag == 'Value':
                        return {'response': True, 'price': x.text}
    else:
        return {'response': False, 'price': None}