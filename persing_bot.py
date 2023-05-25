from aiogram import Bot, Dispatcher, types ,executor
from dotenv import load_dotenv 
from bs4 import BeautifulSoup
import os , logging, requests

load_dotenv('.env')

bot =  Bot(os.environ.get("TOKEN1"))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.reply(f'Hello {message.from_user.full_name}')

@dp.message_handler(commands='start')
async def get_currency(message:types.Message):
    await message.answer(f"Вот текущие данные: ")



executor.start_polling(dp,skip_updates=True)