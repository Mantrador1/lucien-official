﻿# ÎˆÎ»ÎµÎ³Ï‡Î¿Ï‚ Î±Î½ Ï„Î¿ API_KEY ÎµÎ¯Î½Î±Î¹ Î¿ÏÎ¹ÏƒÎ¼Î­Î½Î¿
if (-not $env:API_KEY -or $env:API_KEY -eq "") {
    Write-Host "âŒ ERROR: Î— Î¼ÎµÏ„Î±Î²Î»Î·Ï„Î® Ï€ÎµÏÎ¹Î²Î¬Î»Î»Î¿Î½Ï„Î¿Ï‚ API_KEY Î´ÎµÎ½ ÎµÎ¯Î½Î±Î¹ Î¿ÏÎ¹ÏƒÎ¼Î­Î½Î· Î® ÎµÎ¯Î½Î±Î¹ ÎºÎµÎ½Î®."
    Write-Host "Î Î±ÏÎ±ÎºÎ±Î»ÏŽ Ï€ÏÏŒÏƒÎ¸ÎµÏƒÎµ Ï„Î¿ API_KEY ÏƒÏ„Î¿ Î±ÏÏ‡ÎµÎ¯Î¿ .env Î® ÏŒÏÎ¹ÏƒÎµ Ï„Î¿ Ï‡ÎµÎ¹ÏÎ¿ÎºÎ¯Î½Î·Ï„Î± Î¼Îµ:"
    Write-Host '$env:API_KEY="Ï„Î¿_ÎºÎ»ÎµÎ¹Î´Î¯_ÏƒÎ¿Ï…_ÎµÎ´ÏŽ"'
    exit 1
} else {
    Write-Host "âœ… Î¤Î¿ API_KEY Î­Ï‡ÎµÎ¹ Î¿ÏÎ¹ÏƒÏ„ÎµÎ¯ ÏƒÏ‰ÏƒÏ„Î¬."
}

# Î•ÎºÎºÎ¯Î½Î·ÏƒÎ· Flask server
Write-Host "ðŸš€ Î•ÎºÎºÎ¯Î½Î·ÏƒÎ· Flask server..."
python main.py

