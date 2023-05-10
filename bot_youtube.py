from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from pytube import YouTube
from dotenv import load_dotenv
import os, logging

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

buttons = [
    KeyboardButton('/video'),
    KeyboardButton('/audio')
]
keyboard_one = ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)

@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    await message.answer(f"Привет {message.from_user.full_name}!\nЯ могу скачать видео и аудио из YouTube", reply_markup=keyboard_one)

class VideoState(StatesGroup):
    download = State()

@dp.message_handler(commands='video')
async def get_url_video(message:types.Message):
    await message.reply("Отправьте ссылку на видео и я вам его скачаю в mp4 формате")
    await VideoState.download.set()

@dp.message_handler(commands='audio')
async def get_url_video(message:types.Message):
    await message.reply("Отправьте ссылку на видео и я вам его скачаю в mp4 формате")
    await VideoState.download.set()

@dp.message_handler(state=VideoState.download)
async def download_video(message: types.Message, state: FSMContext):
    url = message.text
    yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
    yt.streams.filter(progressive=True, file_extension="mp4").first().download("video", f"{yt.title}.mp4")
    yt.streams.filter(only_audio=True).first().download("audio", f"{yt.title}.mp3")
    title = yt.title
    video = open(f"video/{title}.mp4", "rb")
    audio = open(f"audio/{title}.mp3", "rb")

    await bot.send_video(message.chat.id, video)
    await bot.send_audio(message.chat.id, audio)

    os.remove(f'video/{title}.mp4')
    os.remove(f'audio/{title}.mp3')
    video.close()
    await state.finish()
    
# @dp.message_handler(lambda message: 'youtube.com/' in message.text)
# async def youtube_handler(message: types.Message):
   
    # video_url = message.text
    # await message.answer('Скачиваю и отправляю видео...')
    # await download_and_send_video(video_url, message.chat.id)
    # await message.answer('Готово!')
    # yt = YouTube( use_oauth=True,allow_oauth_cache=True)
    # yt.streams.filter(progressive=True,file_extension="mp4").order_by('resolution').desc().first().download()
    # with open(yt, 'rb') as f:
    #     msg = await bot.send_video( f)
    #     # Удаляем файл после отправки
    #     os.remove(yt)

# @dp.message_handler(state=VideoState.download)
# async def download_video(message:types.Message, state:FSMContext):
#     if message.text == "Geeks":
#         await message.answer("Go")
#     else:
#         await message.answer("Я вас понял")
#     await state.finish()

@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply("Я вас не понял")

executor.start_polling(dp, skip_updates=True)