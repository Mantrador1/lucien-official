$env:TELEGRAM_BOT_TOKEN = "7121107982:AAHEs4EGv57F2J3kI8AxFeTKHFY5hgq8yX8"
$env:CHAT_ID = "5370071479"

$agents = @(
    @{ Name = "main.py";     Script = "start_helper.ps1" },
    @{ Name = "watchdog";    Script = "start_watchdog.ps1" },
    @{ Name = "stealth";     Script = "start_stealth.ps1" }
)

function Send-Telegram {
    param ($msg)
    try {
        $url = "https://api.telegram.org/bot$($env:TELEGRAM_BOT_TOKEN)/sendMessage"
        $params = @{
            chat_id = $env:CHAT_ID
            text    = $msg
        }
        Invoke-RestMethod -Uri $url -Method POST -Body $params
    } catch {
        Write-Host "[Telegram Error] $_"
    }
}

while ($true) {
    foreach ($agent in $agents) {
        $running = Get-Process | Where-Object { $_.Path -like "*$($agent.Name)*" }
        if (!$running) {
            Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File `"$PWD\$($agent.Script)`"" -WindowStyle Hidden
            Send-Telegram "⚠️ Lucien restarted agent: $($agent.Name)"
        }
    }
    Start-Sleep -Seconds 300  # κάθε 5 λεπτά
}

