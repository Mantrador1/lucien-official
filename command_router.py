﻿# command_router.py

from memory import get_last_messages

def route_command(chat_id, command):
    if command.startswith("/start"):
        return "ðŸš€ LucienX ÎµÎ½ÎµÏÎ³Î¿Ï€Î¿Î¹Î®Î¸Î·ÎºÎµ. Î ÎµÏ‚ Î¼Î¿Ï… ÎºÎ¬Ï„Î¹."

    if command.startswith("/help"):
        return "â„¹ï¸ Î”Î¹Î±Î¸Î­ÏƒÎ¹Î¼ÎµÏ‚ ÎµÎ½Ï„Î¿Î»Î­Ï‚: /start, /help, /whoami, /recall, /reset"

    if command.startswith("/whoami"):
        return f"Î•Î¯ÏƒÎ±Î¹ Î¿ Ï‡ÏÎ®ÏƒÏ„Î·Ï‚ Î¼Îµ chat_id: {chat_id}"

    if command.startswith("/recall"):
        messages = get_last_messages(chat_id)
        if not messages:
            return "â— Î”ÎµÎ½ Î¸Ï…Î¼Î¬Î¼Î±Î¹ Ï„Î¯Ï€Î¿Ï„Î± Î±ÎºÏŒÎ¼Î± Î±Ï€ÏŒ ÎµÏƒÎ­Î½Î±."
        return "ðŸ§  Î¤Î± Ï„ÎµÎ»ÎµÏ…Ï„Î±Î¯Î± ÏƒÎ¿Ï… Î¼Î·Î½ÏÎ¼Î±Ï„Î±:\n" + "\n".join(f"â€¢ {msg}" for msg in messages)

    if command.startswith("/reset"):
        return "ðŸ”„ Î— Î¼Î½Î®Î¼Î· Î¼Î¿Ï… Î¸Î± ÎºÎ±Î¸Î±ÏÎ¹ÏƒÏ„ÎµÎ¯ (ÏŒÏ„Î±Î½ Ï…Î»Î¿Ï€Î¿Î¹Î·Î¸ÎµÎ¯)."

    return f"â“ Î”ÎµÎ½ ÎºÎ±Ï„Î±Î»Î±Î²Î±Î¯Î½Ï‰ Ï„Î·Î½ ÎµÎ½Ï„Î¿Î»Î®: {command}"
