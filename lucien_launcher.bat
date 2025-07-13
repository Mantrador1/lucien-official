@echo off
echo ----------------------------- >> logs\lucien.log
echo [%date% %time%] Starting Lucien Telegram Bot... >> logs\lucien.log
cd /d C:\lucien_proxy
start "" /min cmd /c "python telegram_listener.py >> logs\telegram_listener.log 2>&1"
