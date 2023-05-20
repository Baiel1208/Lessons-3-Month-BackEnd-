from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

load_dotenv('.env')

bot = Bot(os.environ.get('TOKEN1'))
storage = MemoryStorage()
dp = Dispatcher(bot=bot,storage=storage)
database = sqlite3.connect('telegram.db')
cursor = database.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id_user INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    username VARCHAR(100),
    phone_number INTEGER
);
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS address(
    id_user INT,
    address_longitude VARCHAR(100),
    address_latitude VARCHAR(100)
);
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
    title INT,
    address_destination VARCHAR(100),
    date_time_order VARCHAR(100)
);
""")
cursor.connection.commit()

inline_buttons = [
    InlineKeyboardButton('Отправить номер',callback_data='inline_num'),
    InlineKeyboardButton('Отправить локацию', callback_data='inline_loc'),
    InlineKeyboardButton(' Заказать еду', callback_data='inline_food')
]
inlines = InlineKeyboardMarkup().add(*inline_buttons)

class NumState(StatesGroup):
    phone_num = State()

@dp.callback_query_handler(lambda num: num.data == 'inline_num')
async def inline_num(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Пожалуйста, отправьте свой номер телефона.", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def handle_contact(message: types.Message):
    cursor.execute(f"UPDATE users SET phone_number = {message.contact.phone_number} WHERE id_user = {message.from_user.id};")
    cursor.connection.commit()
    if len(message.text) == 13 and message.text[1:].isdigit() and message.text[0] == "+":
        await message.answer("Номер телефона успешно добавлен!")
    
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    cursor=database.cursor()
    cursor.execute(f"SELECT id_user FROM users WHERE id_user = {message.from_user.id};")
    res = cursor.fetchall()
    if res == []:
        cursor.execute(f"""INSERT INTO users VALUES (
            {message.from_user.id},
            '{message.from_user.first_name}',
            '{message.from_user.last_name}',
            '{message.from_user.username}',
            NULL
        )
        """)
        cursor.connection.commit()
    await message.answer(f'Здравствуйте {message.from_user.full_name}.\nМожете заказать еду.',reply_markup=inlines)
        





if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)