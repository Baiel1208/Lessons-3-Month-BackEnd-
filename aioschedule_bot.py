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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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

@dp.message_handler(commands='start')
async def start(message:types.Message):
    # cursor=database.cursor()
    # cursor.execute(f"""INSERT INTO users id VALUES ({message.from_user.id},);""")
    # cursor.connection.commit()
    await message.answer(f"Привет! {message.from_user.full_name}\nМожете добавить свою задачу.",reply_markup=inkb)

@dp.callback_query_handler(lambda call:call)
async def inline(call):
    if call.data == 'inline_title':
        await inline_title(call.message)


@dp.callback_query_handler(text=['inline_title'])
async def inline_title(message:types.Message):
    
    await FSMList.title.set()
    await bot.answer_callback_query( "Введите задачу:")
    await FSMList.next()
    message.answer("Введите время: ")
    

@dp.callback_query_handler(state=FSMList.time)
async def send_title(message: types.Message, state: FSMContext):
    # await FSMList.time.set()
    # cursor = database.cursor()
    # cursor.execute("""UPDATE tasks SET title = ? WHERE id = ?""", (message.from_user.id))
    # cursor.connection.commit()
    message.answer('Задача сохранен')
    await state.finish()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)