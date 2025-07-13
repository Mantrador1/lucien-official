# -*- coding: utf-8 -*-
import telebot
import io, contextlib, os, time, traceback

# ÃƒÅ½Ã¢â‚¬Â¢ÃƒÅ½Ã‚Â´ÃƒÂÃ…Â½ ÃƒÅ½Ã‚Â²ÃƒÅ½Ã‚Â¬ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Âµ ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¿ ÃƒÅ½Ã‚Â´ÃƒÅ½Ã‚Â¹ÃƒÅ½Ã‚ÂºÃƒÂÃ…â€™ ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â¿ÃƒÂÃ¢â‚¬Â¦ TOKEN ÃƒÂÃ¢â€šÂ¬ÃƒÅ½Ã‚Â¿ÃƒÂÃ¢â‚¬Â¦ ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â¿ÃƒÂÃ¢â‚¬Â¦ ÃƒÅ½Ã‚Â­ÃƒÅ½Ã‚Â´ÃƒÂÃ¢â‚¬Â°ÃƒÂÃ†â€™ÃƒÅ½Ã‚Âµ ÃƒÅ½Ã‚Â¿ BotFather
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

print("Lucien Executor v9 running...")

def exec_py(code):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            exec(code, {})
    except Exception as e:
        buf.write("Error: " + str(e))
    return buf.getvalue()

def exec_sh(cmd):
    try:
        out = os.popen(cmd).read()
        return out if out else "Done."
    except Exception as e:
        return "Shell Error: " + str(e)

@bot.message_handler(commands=['start'])
def handle_start(msg):
    bot.reply_to(msg, "Executor ready. Use /code or /run.")

@bot.message_handler(func=lambda msg: msg.text and msg.text.startswith("/code "))
def handle_code(msg):
    result = exec_py(msg.text[6:])
    bot.reply_to(msg, "PYTHON OUTPUT:\n" + result[:2000])

@bot.message_handler(func=lambda msg: msg.text and msg.text.startswith("/run "))
def handle_run(msg):
    result = exec_sh(msg.text[5:])
    bot.reply_to(msg, "SHELL OUTPUT:\n" + result[:2000])

@bot.message_handler(func=lambda msg: True)
def handle_all(msg):
    bot.reply_to(msg, "Unknown command. Use /code or /run.")

def main():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception:
            traceback.print_exc()
            time.sleep(5)

if __name__ == "__main__":
    main()





