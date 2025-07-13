$env:AGENT_ROLE = "watchdog"
$env:OPENROUTER_API_KEY = "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"
$env:TELEGRAM_BOT_TOKEN = "7121107982:AAHEs4EGv57F2J3kI8AxFeTKHFY5hgq8yX8"
$env:CHAT_ID = "5370071479"

Start-Process python -ArgumentList "main.py" `
    -NoNewWindow `
    -RedirectStandardOutput ".\logs\watchdog.log" `
    -RedirectStandardError ".\logs\watchdog_err.log"

