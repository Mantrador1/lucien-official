import telebot

BOT_TOKEN = "7121107982:AAHEs4EGv57F2J3kI8AxFeTKHFY5hgq8yX8"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(f" CHAT ID = {message.chat.id} | USER = {message.from_user.first_name}: {message.text}")

print(" Περιμένω μήνυμα στο bot...")
bot.polling()
