# from pytube import YouTube

# url = input("URL: ")
# yt = YouTube(url, use_oauth=True,allow_oauth_cache=True)
# yt.streams.filter(progressive=True,file_extension="mp4").order_by('resolution').desc().first().download()
# yt.streams.filter(only_audio=True).first().download('audio',f'{yt.title}.,mp3')
import os
import asyncio
import logging
import aiogram 
from aiogram import executor
import pytube

# Инициализация бота
TOKEN = '5676992725:AAGNqjqn9Mxb5cnUBFq2WxtOXdXVBxEk5lY'
bot = aiogram.Bot(TOKEN)
dp = aiogram.Dispatcher(bot)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Определение функции для скачивания и отправки видео
async def download_and_send_video(video_url: str, chat_id: int):
    # Создаем директорию video, если ее еще нет
    if not os.path.exists('video'):
        os.mkdir('video')

    # Скачиваем видео
    video = pytube.YouTube(video_url).streams.filter(file_extension='mp4').first()
    video_path = video.download('video')

    # Отправляем видео пользователю
    with open(video_path, 'rb') as f:
        msg = await bot.send_video(chat_id, f)

    # Удаляем файл после отправки
    os.remove(video_path)

    return msg

# Обработка сообщений
@dp.message_handler(commands=['start'])
async def start_handler(message: aiogram.types.Message):
    await message.answer('Привет! Отправьте мне ссылку на видео на YouTube')

@dp.message_handler(lambda message: 'youtube.com/' in message.text)
async def youtube_handler(message: aiogram.types.Message):
    # Получаем ссылку на видео из сообщения
    video_url = message.text

    # Скачиваем и отправляем видео пользователю
    await message.answer('Скачиваю и отправляю видео...')
    await download_and_send_video(video_url, message.chat.id)
    await message.answer('Готово!')

# Запуск бота
if __name__ == '__main__':
    # executor = Executor(dp)
    executor.start_polling()

