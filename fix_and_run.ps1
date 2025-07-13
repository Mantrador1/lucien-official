$wallet = "wallet1"
$cookieTxt = "C:\lucien_proxy\playwright_stealth\proxie\$wallet.txt"
$cookieJson = "C:\lucien_proxy\playwright_stealth\cookies_ready\$wallet.cookies.json"
$python = "C:\lucien_proxy\venv\Scripts\python.exe"
$runner = "C:\lucien_proxy\playwright_stealth\galxe_runner.py"

# Μετατροπή .txt σε .json cookie
if (Test-Path $cookieTxt) {
    $raw = Get-Content $cookieTxt -Raw
    if ($raw.Trim().Length -eq 0) {
        Write-Host "Το cookie .txt είναι κενό."; pause; exit
    }
    $json = @"
[
  {
    "name": "cf_clearance",
    "value": "$raw",
    "domain": ".galxe.com",
    "path": "/",
    "expires": 1720000000,
    "httpOnly": true,
    "secure": true,
    "sameSite": "Lax"
  }
]
"@
    $json | Set-Content -Encoding UTF8 -Force $cookieJson
    Write-Host "Το cookie μετατράπηκε σε JSON."
} else {
    Write-Host "Δεν βρέθηκε το $cookieTxt"; pause; exit
}

# Καθαρισμός αρχείου από σύμβολα Unicode (emojis)
(Get-Content $runner -Raw) -replace '[^\x00-\x7F]', '' | Set-Content -Encoding UTF8 -Force $runner

# Εγκατάσταση playwright
& $python -m pip uninstall undetected-playwright -y
& $python -m pip install -U playwright
& $python -m playwright install chromium

# Τερματισμός παλιών διεργασιών
Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.Path -like "*python.exe" -and $_.StartInfo.Arguments -like "*galxe_runner.py*"
} | Stop-Process -Force

# Εντολή εκτέλεσης
$cmd = "`"$python`" `"$runner`" --wallet `"$wallet`" --cookie `"$cookieJson`""
Write-Host "`nΕκτελείται:`n$cmd`n"
Invoke-Expression $cmd

pause
