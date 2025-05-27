import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")  # получаем токен из переменной среды
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # Telegram ID администратора

bot = telebot.TeleBot(TOKEN)
user_dict = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Напиши свой вопрос, и я передам его оператору.")

@bot.message_handler(func=lambda msg: True)
def forward_to_admin(message):
    user_id = message.chat.id
    forwarded = bot.forward_message(ADMIN_ID, user_id, message.message_id)
    user_dict[forwarded.message_id] = user_id

@bot.message_handler(func=lambda msg: msg.reply_to_message is not None and msg.chat.id == ADMIN_ID)
def reply_to_user(message):
    original_msg_id = message.reply_to_message.message_id
    if original_msg_id in user_dict:
        user_id = user_dict[original_msg_id]
        bot.send_message(user_id, message.text)

bot.polling()
