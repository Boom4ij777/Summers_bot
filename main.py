import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "7683585782:AAFmSLjtrwGyCEqE7u_OMsInduzfq7KKLEQ"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Чаты по языкам
language_chats = {
    'ru': set(),
    'en': set(),
    'fr': set(),
    'de': set(),
    'it': set(),
    'zh': set()
}

user_language = {}

# Главное меню с кнопками "Чат" и "Время до лета"
main_menu = InlineKeyboardMarkup(row_width=2)
chat_button = InlineKeyboardButton("💬 Чат", callback_data="open_chat_menu")
time_button = InlineKeyboardButton("⏳ Время до лета", callback_data="show_time")
main_menu.add(chat_button, time_button)

# Меню выбора языка
language_menu = InlineKeyboardMarkup(row_width=3)
language_menu.add(
    InlineKeyboardButton("Русский 🇷🇺", callback_data="lang_ru"),
    InlineKeyboardButton("English 🇬🇧", callback_data="lang_en"),
    InlineKeyboardButton("Français 🇫🇷", callback_data="lang_fr"),
    InlineKeyboardButton("Deutsch 🇩🇪", callback_data="lang_de"),
    InlineKeyboardButton("Italiano 🇮🇹", callback_data="lang_it"),
    InlineKeyboardButton("中文 🇨🇳", callback_data="lang_zh")
)

SUMMER_START = datetime(datetime.now().year, 6, 1)

def get_time_to_summer():
    now = datetime.now()
    if now > SUMMER_START:
        summer_next = datetime(now.year + 1, 6, 1)
        delta = summer_next - now
    else:
        delta = SUMMER_START - now
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{days}д {hours}ч {minutes}м {seconds}с"

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Выбери действие:", reply_markup=main_menu)

@dp.callback_query_handler(lambda c: c.data == "open_chat_menu")
async def open_chat_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Выбери язык чата:", reply_markup=language_menu)

@dp.callback_query_handler(lambda c: c.data.startswith('lang_'))
async def join_language_chat(callback_query: types.CallbackQuery):
    lang = callback_query.data.split('_')[1]
    user_id = callback_query.from_user.id

    for chat in language_chats.values():
        chat.discard(user_id)

    language_chats[lang].add(user_id)
    user_language[user_id] = lang

    await bot.answer_callback_query(callback_query.id, text=f"Ты вошёл в чат на языке: {lang}")
    await bot.send_message(user_id, f"Теперь все твои сообщения будут видны только участникам {lang}-чата.")

@dp.callback_query_handler(lambda c: c.data == "show_time")
async def show_time(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    sent_message = await bot.send_message(callback_query.from_user.id, "Считаю время до лета...")

    while True:
        timer_text = f"Время до лета: {get_time_to_summer()}"
        try:
            await bot.edit_message_text(timer_text, chat_id=sent_message.chat.id, message_id=sent_message.message_id)
        except Exception as e:
            break
        await asyncio.sleep(1)

@dp.message_handler()
async def language_chat_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_language and not message.text.startswith('/'):
        lang = user_language[user_id]
        chat_members = language_chats.get(lang, set())
        for uid in chat_members:
            if uid != user_id:
                try:
                    await bot.send_message(uid, f"{message.from_user.first_name} [{lang}]: {message.text}")
                except:
                    pass

if __name__ == '__main__':
    executor.start_polling(dp)