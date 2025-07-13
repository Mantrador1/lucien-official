# -*- coding: utf-8 -*-
import telebot
import sys, io, contextlib, os, time, traceback

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

print("ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Lucien Executor v9 online and monitoring Telegram...")

def execute_python(code):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            exec(code, {})
    except Exception as e:
        buf.write(f"ÃƒÂ¢Ã‚ÂÃ…â€™ Error: {e}")
    return buf.getvalue()

def execute_shell(cmd):
    try:
        out = os.popen(cmd).read()
        return out or "ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ ÃƒÅ½Ã…Â¸ÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â¿ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Â»ÃƒÅ½Ã‚Â·ÃƒÂÃ‚ÂÃƒÂÃ…Â½ÃƒÅ½Ã‚Â¸ÃƒÅ½Ã‚Â·ÃƒÅ½Ã‚ÂºÃƒÅ½Ã‚Âµ ÃƒÂÃ¢â‚¬Â¡ÃƒÂÃ¢â‚¬Â°ÃƒÂÃ‚ÂÃƒÅ½Ã‚Â¯ÃƒÂÃ¢â‚¬Å¡ output."
    except Exception as e:
        return f"ÃƒÂ¢Ã‚ÂÃ…â€™ Shell Error: {e}"

@bot.message_handler(commands=['start'])
def on_start(m):
    bot.reply_to(m, "Lucien Executor v9 ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚ÂµÃƒÂÃ‚ÂÃƒÅ½Ã‚Â³ÃƒÂÃ…â€™. /code ÃƒÅ½Ã‚Â® /run ÃƒÅ½Ã‚Â® /apk")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("/code "))
def on_code(m):
    res = execute_python(m.text[6:])
    bot.reply_to(m, f"ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â¤ Python:
{res[:4000]}")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("/run "))
def on_run(m):
    res = execute_shell(m.text[5:])
    bot.reply_to(m, f"ÃƒÂ°Ã…Â¸Ã¢â‚¬â„¢Ã‚Â» Shell:
{res[:4000]}")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("/apk"))
def on_apk(m):
    bot.reply_to(m, "ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â¦ APK module ÃƒÅ½Ã‚ÂµÃƒÅ½Ã‚Â½ÃƒÅ½Ã‚ÂµÃƒÂÃ‚ÂÃƒÅ½Ã‚Â³ÃƒÂÃ…â€™. ÃƒÅ½Ã‚Â£ÃƒÂÃ‚ÂÃƒÅ½Ã‚Â½ÃƒÂÃ¢â‚¬Å¾ÃƒÅ½Ã‚Â¿ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â± Kotlin & base64.")

@bot.message_handler(func=lambda m: True)
def on_fallback(m):
    bot.reply_to(m, "ÃƒÂ¢Ã‚ÂÃ¢â‚¬Å“ ÃƒÅ½Ã‚Â§ÃƒÂÃ‚ÂÃƒÅ½Ã‚Â·ÃƒÂÃ†â€™ÃƒÅ½Ã‚Â¹ÃƒÅ½Ã‚Â¼ÃƒÅ½Ã‚Â¿ÃƒÂÃ¢â€šÂ¬ÃƒÅ½Ã‚Â¿ÃƒÅ½Ã‚Â¯ÃƒÅ½Ã‚Â·ÃƒÂÃ†â€™ÃƒÅ½Ã‚Âµ /code, /run ÃƒÅ½Ã‚Â® /apk")

def run():
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            traceback.print_exc()
            time.sleep(5)

if __name__ == "__main__":
    run()





