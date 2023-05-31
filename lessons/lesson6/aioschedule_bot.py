from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os, aioschedule, requests, logging, asyncio,sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
load_dotenv('.env')

bot = Bot(os.environ.get('TOKEN1'))
storage = MemoryStorage()
dp = Dispatcher(bot=bot,storage=storage)


database = sqlite3.connect('list.db')
cursor = database.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER,
        username TEXT,
        title TEXT,
        time TEXT
    );
''')
cursor.connection.commit()

inkb = InlineKeyboardMarkup()
ikb = [
    InlineKeyboardButton("Добавить задачу", callback_data="inline_title"),
    InlineKeyboardButton("Удалить задачу", callback_data="inline_delete")
]

inkb.add(*ikb)

class FSMList(StatesGroup):
    title = State()
    time = State()

@dp.callback_query_handler(lambda call:call)
async def inline(call):
    if call.data == 'inline_title':
        await inline_title(call.message)


@dp.message_handler(commands='start')
async def start(message:types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    cursor.execute("INSERT INTO tasks (id, username) VALUES (?, ?)", (user_id, username))
    cursor.connection.commit()

    cursor.connection.close()
    await message.answer(f"Привет! {message.from_user.full_name}\nМожете добавить свою задачу.",reply_markup=inkb)


@dp.callback_query_handler(text=['inline_title'])
async def inline_title(message:types.Message):
    await message.answer("Введите задачу:")
    await FSMList.title.set()

@dp.message_handler(state=FSMList.title)
async def send_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
        cursor.execute(f'INSERT INTO tasks (title) VALUES (?)', {message.title})
        # cursor.execute('''SELECT * FROM tasks WHERE title;''')
        # cursor.fetchall()
        # cursor.execute("SELECT * FROM tasks").fetchall()
        # cursor.connection.commit()

    await message.answer("Укажите время")
    await FSMList.next()


@dp.message_handler(state=FSMList.time)
async def send_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text
    await message.answer("Задача сохранен")
    await state.finish()

# @dp.callback_query_handler(state=FSMList.title)
# async def send_title(message: types.Message, state: FSMContext):

    # cursor = database.cursor()
    # cursor.execute("""UPDATE tasks SET title = ? WHERE id = ?""", (message.from_user.id))
    # cursor.connection.commit()
    # message.answer('Задача сохранен')
    # await FSMList.next()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)