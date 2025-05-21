from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime

TOKEN = '7683585782:AAFmSLjtrwGyCEqE7u_OMsInduzfq7KKLEQ'  # ТВОЙ ТОКЕН

texts = {
    'ru': {
        'choose_lang': "Выберите язык:",
        'summer_time': "До лета осталось: {time}",
        'language_set': "Язык установлен на русский.",
        'update': "Обновить",
    },
    'en': {
        'choose_lang': "Choose a language:",
        'summer_time': "Time until summer: {time}",
        'language_set': "Language set to English.",
        'update': "Update",
    },
    'fr': {
        'choose_lang': "Choisissez une langue :",
        'summer_time': "Temps jusqu'à l'été : {time}",
        'language_set': "Langue définie sur le français.",
        'update': "Actualiser",
    },
    'zh': {
        'choose_lang': "请选择语言：",
        'summer_time': "距离夏天还有：{time}",
        'language_set': "语言已设置为中文。",
        'update': "刷新",
    },
    'de': {
        'choose_lang': "Sprache wählen:",
        'summer_time': "Zeit bis zum Sommer: {time}",
        'language_set': "Sprache auf Deutsch gesetzt.",
        'update': "Aktualisieren",
    },
    'it': {
        'choose_lang': "Scegli una lingua:",
        'summer_time': "Tempo fino all'estate: {time}",
        'language_set': "Lingua impostata su italiano.",
        'update': "Aggiorna",
    },
}

user_lang = {}

def get_time_until_summer():
    now = datetime.now()
    summer = datetime(now.year, 6, 1)
    if now >= summer:
        summer = datetime(now.year + 1, 6, 1)
    delta = summer - now
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    seconds = delta.seconds % 60
    return f"{days}д {hours}ч {minutes}м {seconds}с"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("English", callback_data="lang_en")],
        [InlineKeyboardButton("Français", callback_data="lang_fr")],
        [InlineKeyboardButton("中文", callback_data="lang_zh")],
        [InlineKeyboardButton("Deutsch", callback_data="lang_de")],
        [InlineKeyboardButton("Italiano", callback_data="lang_it")]
    ])
    await update.message.reply_text(texts['en']['choose_lang'], reply_markup=keyboard)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id

    if data.startswith("lang_"):
        lang = data.split("_")[1]
        user_lang[user_id] = lang
        await query.answer()
        await query.edit_message_text(texts[lang]['language_set'])

        time_str = get_time_until_summer()
        text = texts[lang]['summer_time'].format(time=time_str)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(texts[lang]['update'], callback_data="refresh")]
        ])
        await query.message.reply_text(text, reply_markup=keyboard)

    elif data == "refresh":
        lang = user_lang.get(user_id, 'en')
        time_str = get_time_until_summer()
        text = texts[lang]['summer_time'].format(time=time_str)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(texts[lang]['update'], callback_data="refresh")]
        ])
        await query.answer()
        await query.edit_message_text(text, reply_markup=keyboard)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Бот запущен")
    app.run_polling()

if __name__ == '__main__':
    main()