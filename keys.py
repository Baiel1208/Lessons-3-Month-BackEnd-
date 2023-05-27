from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn = [ 
    InlineKeyboardButton('USD', callback_data='USD'),
    InlineKeyboardButton('EURO', callback_data='EURO'),
    InlineKeyboardButton('RUB', callback_data='RUB'),
    InlineKeyboardButton('KZT', callback_data='KZT')
]
button = InlineKeyboardMarkup().add(*btn)


btn2 = [
    InlineKeyboardButton('Ввести собственую сумму', callback_data='me_cymma')
]
me_sum = InlineKeyboardMarkup().add(*btn2)





# @dp.message_handler(commands='currency')
# async def get_currency(message:types.Message):
#     url = 'https://www.nbkr.kg/index.jsp?lang=RUS'
#     responce =requests.get(url)
#     soup=BeautifulSoup(responce.text, 'lxml')
#     currency = soup.find_all('td', class_='exrate')
#     for usd in currency[0:1]:
#         usd_currency = usd.text
#     for eur in currency[2:3]:
#         eur_currency = eur.text
#     for rub in currency[4:5]:
#         rub_currency = rub.text
#     for kzt in currency[6:7]:
#         kzt_currency = kzt.text
#     await message.answer(f"""Вот текущие данные:
# USD:{usd_currency}
# EUR:{eur_currency}
# RUB:{rub_currency}
# KZT:{kzt_currency}""")