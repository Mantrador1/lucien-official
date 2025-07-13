# -*- coding: utf-8 -*-
import telebot
import subprocess

# Token
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ¢â‚¬Å“ Lucien Core online. Send /run <command> or /code <python>")

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    user_input = message.text.strip()

    if user_input.startswith("/run "):
        command = user_input[5:]
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True, timeout=10)
        except subprocess.CalledProcessError as e:
            result = f"[ÃƒÂ¢Ã‚ÂÃ…â€™ Error]\n{e.output}"
        except Exception as e:
            result = f"[ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â Exception] {e}"
        bot.reply_to(message, f"[ÃƒÂ°Ã…Â¸Ã¢â‚¬â€œÃ‚Â¥ Output]\n{result}")

    elif user_input.startswith("/code "):
        code = user_input[6:]
        try:
            exec_locals = {}
            exec(code, {}, exec_locals)
            result = exec_locals.get("result", "[ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Executed]")
        except Exception as e:
            result = f"[ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â Exception] {e}"
        bot.reply_to(message, str(result))

    else:
        bot.reply_to(message, f"ÃƒÂ°Ã…Â¸Ã…Â¸Ã‚Â¢ Lucien ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â´ÃƒÂÃ…Â½. ÃƒÅ½Ã‚Â£ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â¯ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Âµ `/run` ÃƒÅ½Ã‚Â³ÃƒÅ½Ã‚Â¹ÃƒÅ½Ã‚Â± command ÃƒÅ½Ã‚Â® `/code` ÃƒÅ½Ã‚Â³ÃƒÅ½Ã‚Â¹ÃƒÅ½Ã‚Â± Python.")

print("ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Lucien Bot with Executor running...")
bot.polling()





