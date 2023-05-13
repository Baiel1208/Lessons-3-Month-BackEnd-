from aiogram import Bot, Dispatcher, types, executor
import random
import os


bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    await message.answer("Я загадал число от 1 до 3, отгадай: ")


@dp.message_handler(text=['1', '2', '3'])
async def play(message:types.Message):
    num = random.randint(1, 3)
    if int(message.text) == num:
        await message.reply('Вы угадали!')
    else:
        await message.reply(f'Неправильно. Число было {num}.')


executor.start_polling(dp, skip_updates=True)
