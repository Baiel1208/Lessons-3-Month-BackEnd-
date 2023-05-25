from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
import sqlite3, logging, smtplib, os 

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

inline_keyboards = [
    InlineKeyboardButton('Отправить сообщение', callback_data='send_mail')
]

inline = InlineKeyboardMarkup().add(*inline_keyboards)

class EmailState(StatesGroup):
    mail = State()
    subject = State()
    message = State()

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Hello World", reply_markup=inline)

@dp.callback_query_handler(lambda call: call)
async def all_inline(call):
    if call.data == 'send_mail':
        await send_bot_mail(call.message)

@dp.message_handler(commands='send')
async def send_bot_mail(message:types.Message):
    await message.answer("Почта:")
    await EmailState.mail.set()

@dp.message_handler(state=EmailState.mail)
async def get_subject(message:types.Message, state:FSMContext):
    await state.update_data(mail=message.text)
    await message.answer("Введите заголовок:")
    await EmailState.subject.set()

@dp.message_handler(state=EmailState.subject)
async def get_message(message:types.Message, state:FSMContext):
    await state.update_data(subject=message.text)
    await message.answer("Введите сообщение:")
    await EmailState.message.set()

@dp.message_handler(state=EmailState.message)
async def send_message(message:types.Message, state:FSMContext):
    await state.update_data(message=message.text)
    await message.answer("Отправляется сообщение")
    data = await state.get_data()
    mail = data['mail']
    subject = data['subject']
    message_text = data['message']
    await EmailState.message.set()

    try:
        smtp_host = 'smtp.gmail.com'
        smtp_port = 587
        smtp_login = os.environ.get('smtp_email')
        password = os.environ.get('smtp_password')
        sender = os.environ.get('smtp_email')
        recipient_email = '@gmail.com'

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_login, password)
            
            email_text = f"Subject: {subject}\n\n{message_text}"
            server.sendmail(sender, recipient_email, email_text)
        
        await message.answer("Сообщение успешно отправлено!")
    except Exception as file:
        await message.answer(f"Ошибка при отправке сообщения: {str(file)}")

    await state.finish()

executor.start_polling(dp, skip_updates=True)
