from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from decouple import config

TOKEN1 = config("TOKEN1")

bot = Bot(token=TOKEN1)
storage = MemoryStorage()
dp = Dispatcher(bot=bot,storage=storage)


buttons1 = [KeyboardButton('/Android'), KeyboardButton('/iOS'),KeyboardButton('/BackEnd'),KeyboardButton('/FrontEnd'),KeyboardButton('/UXUI')]
keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons1)

buttons2 = [KeyboardButton('/cancel')]
keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons2)

inline_buttons1 = [
    InlineKeyboardButton('Android',callback_data='inline_android'),
    InlineKeyboardButton('iOS',callback_data='inline_ios'),
    InlineKeyboardButton('BackEnd',callback_data='inline_backend'),
    InlineKeyboardButton('FrontEnd',callback_data='inline_frontend'),
    InlineKeyboardButton('UXUI',callback_data='inline_uxui')
]
inline = InlineKeyboardMarkup().add(*inline_buttons1)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}! '
                         f'Я могу вам дать информацию о наших направлениях в сфере IT , стоимость курса, месяц обучения', 
                           reply_markup=keyboard1)

@dp.message_handler(commands=['android'], state=None)
async def android(message: types.Message):
    await message.answer(f'Android-разработчик - это специалист, который занимается созданием приложений и программного обеспечения для операционной системы Android. Он использует язык программирования Java, Kotlin или другие языки, поддерживаемые платформой Android\nСтоимость 10000 сом в месяц.\nОбучение: 7 месяц',
                        reply_markup=keyboard2)

@dp.message_handler(text=['/cancel'],)
async def video_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(f'Можете посмотерть другие направление.', reply_markup=keyboard1)

    
@dp.message_handler(commands=['ios'], state=None)
async def ios(message: types.Message):
    await message.answer(f'iOS-разработчик - это специалист, который занимается разработкой приложений для устройств, работающих под управлением операционной системы iOS, разработанной компанией Apple. iOS-разработчик использует язык программирования Swift или Objective-C и инструменты разработки, предоставляемые Apple, такие как Xcode и т.д.\nСтоимость 10000 сом в месяц.\nОбучение: 7 месяц',
                        reply_markup=keyboard2)

@dp.message_handler(commands=['backend'], state=None)
async def backend(message: types.Message):
    await message.answer(f'Backend-разработчик - это специалист, который занимается созданием и поддержкой серверной части программного обеспечения. Он отвечает за разработку и поддержку логики, обработку данных и взаимодействие с базами данных \nСтоимость 10000 сом в месяц.\nОбучение: 5 месяц',
                        reply_markup=keyboard2)

@dp.message_handler(commands=['frontend'], state=None)
async def frontend(message: types.Message):
    await message.answer(f'Frontend-разработчик - это специалист, который занимается разработкой пользовательского интерфейса (UI) веб-приложений. Он отвечает за создание визуальной части приложения, с которой взаимодействует пользователь.\nСтоимость 10000 сом в месяц.\nОбучение: 5 месяц',
                        reply_markup=keyboard2)
    
@dp.message_handler(commands=['uxui'], state=None)
async def uxui(message: types.Message):
    await message.answer(f'UX/UI разработчик (User Experience/User Interface) занимается проектированием и разработкой пользовательского интерфейса (UI) и опыта пользователя (UX) для различных цифровых продуктов, таких как мобильные приложения, веб-сайты, программное обеспечение и другие интерактивные системы.\nСтоимость 10000 сом в месяц.\nОбучение: 5 месяц',
                        reply_markup=keyboard2)


executor.start_polling(dp)
