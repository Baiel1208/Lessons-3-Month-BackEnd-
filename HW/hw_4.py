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
    id_user INTEGER PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    username VARCHAR(100),
    phone_number INTEGER
);
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS address(
    id_user INTEGER PRIMARY KEY,
    address_longitude VARCHAR(100),
    address_latitude VARCHAR(100)
);
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
    title VARCHAR(255),
    address_destination VARCHAR(255),
    date_time_order VARCHAR(255)
);
""")
cursor.connection.commit()

inline_buttons = [
    InlineKeyboardButton('Отправить номер',callback_data='inline_num'),
    InlineKeyboardButton('Отправить локацию', callback_data='inline_loc'),
    InlineKeyboardButton(' Заказать еду', callback_data='inline_food')
]
inlines = InlineKeyboardMarkup().add(*inline_buttons)

class States(StatesGroup):
    phone_number = State()
    location = State()
    title = State()
    
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    cursor=database.cursor()
    cursor.execute(f"SELECT id_user FROM users WHERE id_user = {message.from_user.id};")
    res = cursor.fetchall()
    if not  res:
        cursor.execute(f"""INSERT INTO users (id_user, first_name, last_name, username) VALUES (
            {message.from_user.id},
            '{message.from_user.first_name}',
            '{message.from_user.last_name}',
            '{message.from_user.username}'
        );
        """)
        cursor.connection.commit()
    await message.answer(f'Здравствуйте {message.from_user.full_name}!\nМожете заказать еду.',reply_markup=inlines)
        
@dp.callback_query_handler(text=['inline_num'])
async def phone_number(callbak: types.CallbackQuery):
    await bot.send_message(callbak.message.chat.id, "Введите ваш телефонный номер:")
    await States.phone_number.set()


@dp.message_handler(state=States.phone_number)
async def send_number(message: types.Message, state: FSMContext):
    cursor = database.cursor()
    cursor.execute("""UPDATE users SET phone_number = ? WHERE user_id = ?;""")
    cursor.connection.commit()
    message.answer('Номер сохранен')
    await state.finish()

@dp.callback_query_handler(text=['inline_loc'])
async def location(callbak: types.CallbackQuery):
    await bot.send_message(callbak.message.chat.id, "Отправьте вашу локацию:")
    await States.location.set()


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def save_loc(message: types.Message):
    cursor = database.cursor()
    cursor.execute(f"INSERT INTO address (id_user, address_longitude, address_latitude) VALUES ({message.from_user.id}, '{message.location.longitude}', '{message.location.latitude}');")
    cursor.connection.commit()
    await message.answer("Локация сохранена")


@dp.callback_query_handler(lambda call: call.data == 'inline_food')
async def order_food(call: types.CallbackQuery):
    await call.message.answer('Заказать еду: ')
    await bot.delete_message(call.message.chat.id,call.message.message_id)


@dp.callback_query_handler(text=['inline_food'])
async def order(callbak: types.CallbackQuery):
    cursor = database.cursor()
    cursor.execute(f"INSERT INTO orders (title, address_destination, date_time_order) VALUES ('{callbak.text}', 'адрес', 'дата и время');")
    cursor.connection.commit()
    await callbak.answer('Заказ сохранен')




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)