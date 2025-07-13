$venv = "C:\lucien_proxy\venv"
$python = "$venv\Scripts\python.exe"
$runner = "C:\lucien_proxy\playwright_stealth\galxe_runner.py"
$auditLog = "C:\lucien_proxy\wallet_audit_log.txt"
$cookieDir = "C:\lucien_proxy\playwright_stealth\cookies_ready"
$logFile = "C:\lucien_proxy\execution_status_log.txt"

if (-not (Test-Path $logFile)) {
  New-Item -Path $logFile -ItemType File -Force | Out-Null
}

# Καθαρή εγκατάσταση playwright (όχι stealth)
& $python -m pip uninstall undetected-playwright -y | Out-Null
& $python -m pip install -U playwright | Out-Null
& $python -m playwright install chromium | Out-Null

# Τερματισμός stuck galxe_runner.py
Get-Process python -ErrorAction SilentlyContinue | Where-Object {
  $_.Path -and $_.StartInfo.Arguments -like '*galxe_runner.py*'
} | Stop-Process -Force

# Εκκίνηση farming για όλα τα wallets
Get-Content $auditLog | Where-Object { $_ -match '✅' } | ForEach-Object {
  $wallet = ($_ -split ':')[0].Trim()
  $cookie = Join-Path $cookieDir "$wallet.cookies.json"
  $cmd = "`"$python`" `"$runner`" --cookie `"$cookie`" --wallet `"$wallet`""
  $logOk = "$wallet OK $(Get-Date -Format 'HH:mm:ss')"
  $logFail = "$wallet FAIL $(Get-Date -Format 'HH:mm:ss')"
  $block = "try { Invoke-Expression `"$cmd`"; Add-Content -Path `"$logFile`" -Value `"$logOk`" } catch { Add-Content -Path `"$logFile`" -Value `"$logFail`" }"
  Start-Process powershell -ArgumentList "-NoProfile -Command $block" -WindowStyle Hidden
  Start-Sleep -Milliseconds (Get-Random -Minimum 3000 -Maximum 6000)
}

Write-Host "`n✅ Everything fixed and farming started successfully.`n"
