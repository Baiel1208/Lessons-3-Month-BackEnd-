from aiogram import Bot, Dispatcher,types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from decouple import config
import logging
TOKEN1 = config("TOKEN1")

bot = Bot(TOKEN1)
dp = Dispatcher(bot=bot)



@dp.message_handler(commands=['start'])
async def sart_handler(message:types.Message):
    markup = InlineKeyboardMarkup()
    buttom_1 = InlineKeyboardButton("NEXT",callback_data='buttom_1')
    markup.add(buttom_1)
    question = "Cколько стоит любовь?"  
    answers = [
        "28 - мультов",
        "10 - мультов",
        "20 - мультов",
        "30 - мультов",
        "35 - мультов",
        "25 - мультов"
    ]
    
    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        # open_period=10,
        reply_markup=markup
    )

@dp.callback_query_handler(text='buttom_1')
async def quiz(call:types.CallbackQuery):
    question = "Бека когда не станет бабником?"  
    answers = [
        "Он не бабник",
        "Никогда",
        "Мадина",
        "Муха Топ",
        "Аруукс",
        "Ала-Бука",
        "Чопуля",
        "Чопульяно"
    ]
    
    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        open_period=15,
    )

@dp.message_handler(commands=['meme'])
async def start(message:types.Message):
    await message.answer_photo('https://secretmag.ru/imgs/2022/12/23/15/5726988/1405ca91de75300f7f73fe390d3f1326b7fa0f62.png')
    



@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    await message.answer(f"Hello {message.from_user.full_name}")

@dp.message_handler()
async def echo(message:types.Message):
    await bot.send_message(message.from_user.id,message.text)
    # await message.answer("This is an answer method!")
    # await message.reply("This is an reply method")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)