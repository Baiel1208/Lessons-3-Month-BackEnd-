from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os, aioschedule, requests, logging, asyncio,sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
load_dotenv('.env')

bot = Bot(os.environ.get('TOKEN1'))
storage = MemoryStorage()
dp = Dispatcher(bot=bot,storage=storage)
logging.basicConfig(level=logging.INFO)

database = sqlite3.connect('list.db')
cursor = database.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        time TEXT
    );
''')

class FSMList(StatesGroup):
    title = State()
    time = State()



@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f"Привет! Добавь свою задачу в формате {message.from_user.full_name}")
    try:
        command, title, time = message.text.split()
        task = FSMList(title, time)

        # Сохранение задачи в базе данных
        cursor.execute('INSERT INTO tasks (title, time) VALUES (?, ?)', (task.title, task.time))
        cursor.commit()

        await message.reply("Задача успешно добавлена!")
    except Exception as e:
        await message.reply(f"Ошибка при добавлении задачи: {str(e)}")
    
# async def send_message():
#     await bot.send_message(chat_id=5695269601, text="Hello Geeks")

# async def schedule():
#     aioschedule.every().minutes.do(FSMList.time) 
#     while True:
#         await aioschedule.run_pending()

# async def on_startup(hello):
#     asyncio.create_task(schedule())

# executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
async def send_message():
    await bot.send_message(chat_id=5695269601, text="Hello Geeks")

async def schedule():
    aioschedule.every(0.5).seconds.do(send_message) 
    while True:
        await aioschedule.run_pending()

async def on_startup(hello):
    asyncio.create_task(schedule())

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)