$mainPath = "C:\lucien_proxy\main.py"
$backupPath = "C:\lucien_proxy\main_backup.py"
$botToken = $env:TELEGRAM_BOT_TOKEN
$chatId = $env:CHAT_ID

function Send-Telegram($msg) {
    try {
        Invoke-RestMethod -Uri "https://api.telegram.org/bot$botToken/sendMessage" `
            -Method POST `
            -ContentType "application/json" `
            -Body (@{ chat_id = $chatId; text = $msg } | ConvertTo-Json -Compress)
    } catch {}
}

while ($true) {
    if (!(Test-Path $mainPath)) {
        Copy-Item -Path $backupPath -Destination $mainPath -Force
        Send-Telegram "⚠️ main.py was missing! Restored from backup."
    } elseif ((Get-FileHash $mainPath).Hash -ne (Get-FileHash $backupPath).Hash) {
        Copy-Item -Path $backupPath -Destination $mainPath -Force
        Send-Telegram "⚠️ main.py was modified! Restored from backup."
    }
    Start-Sleep -Seconds 180
}

$secretKey = "5e3c91d2b7f849ddadf84613e06f29f1"
$mainPath = "$PWD\main.py"
$sigPath = "$PWD\main.sig"
$backupPath = "$PWD\main_backup.py"

function Get-HMAC {
    param ([string]$path)
    $hmac = New-Object System.Security.Cryptography.HMACSHA256
    $hmac.Key = [System.Text.Encoding]::UTF8.GetBytes($secretKey)
    $bytes = [System.IO.File]::ReadAllBytes($path)
    return ($hmac.ComputeHash($bytes) | ForEach-Object { $_.ToString("x2") }) -join ""
}

while ($true) {
    try {
        if (!(Test-Path $mainPath) -or !(Test-Path $sigPath)) {
            Copy-Item -Path $backupPath -Destination $mainPath -Force
            $signature = Get-HMAC -path $mainPath
            Set-Content -Path $sigPath -Value $signature
            Send-Telegram "⚠️ ALERT: main.py was missing! Restored and re-signed."
        } else {
            $currentSig = Get-HMAC -path $mainPath
            $expectedSig = Get-Content -Path $sigPath -Raw
            if ($currentSig -ne $expectedSig) {
                Copy-Item -Path $backupPath -Destination $mainPath -Force
                $signature = Get-HMAC -path $mainPath
                Set-Content -Path $sigPath -Value $signature
                Send-Telegram "⚠️ ALERT: main.py was modified! Restored and re-signed."
            }
        }
    } catch {
        Write-Host "[Integrity Watchdog Error] $_"
    }
    Start-Sleep -Seconds 180
}
# 🔐 AES Decryption if needed
function Restore-From-EncryptedBackup {
    $secretKey = "5e3c91d2b7f849ddadf84613e06f29f1"
    $keyBytes = [System.Text.Encoding]::UTF8.GetBytes($secretKey.PadRight(32, '0').Substring(0, 32))
    $encPath = "$PWD\main_backup.enc"
    $mainPath = "$PWD\main.py"

    if (!(Test-Path $encPath)) {
        Send-Telegram "⛔ Encrypted backup missing: main_backup.enc"
        return
    }

    $raw = [System.IO.File]::ReadAllBytes($encPath)
    $iv = $raw[0..15]
    $data = $raw[16..($raw.Length - 1)]
    $aes = [System.Security.Cryptography.Aes]::Create()
    $aes.Mode = "CBC"
    $aes.Key = $keyBytes
    $aes.IV = $iv
    $decryptor = $aes.CreateDecryptor()
    try {
        $decrypted = $decryptor.TransformFinalBlock($data, 0, $data.Length)
        [System.IO.File]::WriteAllBytes($mainPath, $decrypted)
        Send-Telegram "✅ main.py was restored from encrypted backup!"
    } catch {
        Send-Telegram "⛔ Decryption failed: $($_.Exception.Message)"
    }
}
Restore-From-EncryptedBackup

