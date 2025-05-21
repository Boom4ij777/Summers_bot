from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime

TOKEN = '7683585782:AAFmSLjtrwGyCEqE7u_OMsInduzfq7KKLEQ'

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
    return f"До лета осталось: {days}д {hours}ч {minutes}м {seconds}с"

keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Обновить", callback_data="refresh")]]
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = get_time_until_summer()
    await update.message.reply_text(text, reply_markup=keyboard)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = get_time_until_summer()
    await query.edit_message_text(text=text, reply_markup=keyboard)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Бот запущен. Нажми Ctrl+C для остановки.")
    app.run_polling()

if __name__ == "__main__":
    main()