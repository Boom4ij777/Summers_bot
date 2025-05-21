import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '7683585782:AAFmSLjtrwGyCEqE7u_OMsInduzfq7KKLEQ'
ALLOWED_USER_ID = 7817919248  # Твой Telegram ID

checked_users = set()

# Мемы на разных языках
memes = {
    "ru": [
        "Я загружаюсь медленно времени.",
        "Лето ждёт быстро настроения.",
        "Кофе пропадает смешно желания.",
        "Работа горит лениво энергии.",
        "Кот спит странно смысла."
    ],
    "fr": [
        "Je charge lentement le temps.",
        "L'été attend rapidement l'humeur.",
        "Le café disparaît drôlement le désir.",
        "Le travail brûle paresseusement l'énergie.",
        "Le chat dort étrangement le sens."
    ],
    "de": [
        "Ich lade langsam die Zeit.",
        "Der Sommer wartet schnell auf die Stimmung.",
        "Der Kaffee verschwindet lustig den Wunsch.",
        "Die Arbeit brennt faul die Energie.",
        "Die Katze schläft seltsam den Sinn."
    ],
    "it": [
        "Sto caricando lentamente il tempo.",
        "L'estate aspetta rapidamente l'umore.",
        "Il caffè scompare divertente il desiderio.",
        "Il lavoro brucia pigramente l'energia.",
        "Il gatto dorme stranamente il senso."
    ],
    "zh": [
        "我慢慢加载时间。",
        "夏天快速等待心情。",
        "咖啡有趣地消失了欲望。",
        "工作懒惰地燃烧能量。",
        "猫奇怪地睡着了意义。"
    ],
}

def get_time_until_summer():
    now = datetime.now()
    summer = datetime(now.year, 6, 1)
    if now >= summer:
        summer = datetime(now.year + 1, 6, 1)
    delta = summer - now
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    return f"{days}д {hours}ч {minutes}м"

def get_user_lang(user):
    lang = user.language_code if user.language_code else "ru"
    if lang not in memes:
        lang = "ru"
    return lang

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Время до лета + мем", callback_data='time_meme')],
        [InlineKeyboardButton("Список проверивших", callback_data='user_list')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выбери действие:', reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    lang = get_user_lang(user)

    if query.data == 'time_meme':
        checked_users.add(f"{user.first_name} ({user.id})")
        time = get_time_until_summer()
        meme = random.choice(memes[lang])
        response = f"До лета осталось: {time}\nМем: {meme}"
        await query.edit_message_text(response)

    elif query.data == 'user_list':
        if user.id == ALLOWED_USER_ID:
            if checked_users:
                users_text = "\n".join(checked_users)
                await query.edit_message_text(f"Проверяли время до лета:\n{users_text}")
            else:
                await query.edit_message_text("Пока никто не проверял время до лета.")
        else:
            await query.edit_message_text("Извини, этот список доступен только владельцу бота.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Бот запущен")
    app.run_polling()

if __name__ == '__main__':
    main()