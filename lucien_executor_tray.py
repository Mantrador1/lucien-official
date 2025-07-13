# -*- coding: utf-8 -*-
import telebot
import io, contextlib, os, time, traceback

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

print("Executor v9 running...")

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
def on_start(msg):
    bot.reply_to(msg, "Ready. /code or /run")

@bot.message_handler(func=lambda msg: msg.text and msg.text.startswith("/code "))
def on_code(msg):
    res = exec_py(msg.text[6:])
    bot.reply_to(msg, "PYOUT:\n" + res[:2000])

@bot.message_handler(func=lambda msg: msg.text and msg.text.startswith("/run "))
def on_run(msg):
    res = exec_sh(msg.text[5:])
    bot.reply_to(msg, "SHOUT:\n" + res[:2000])

@bot.message_handler(func=lambda msg: True)
def on_all(msg):
    bot.reply_to(msg, "Use /code or /run")

def main():
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            traceback.print_exc()
            time.sleep(5)

if __name__ == "__main__":
    main()





