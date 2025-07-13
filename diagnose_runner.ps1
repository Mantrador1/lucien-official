$wallet = "TEST_ENTRY"
$python = "C:\lucien_proxy\venv\Scripts\python.exe"
$runner = "C:\lucien_proxy\playwright_stealth\galxe_runner.py"
$cookie = "C:\lucien_proxy\playwright_stealth\cookies_ready\$wallet.cookies.json"
$logFile = "C:\lucien_proxy\diagnostic_run_output.txt"

Write-Host "`n🚀 Διάγνωση για wallet: $wallet`n"
& $python $runner --wallet "$wallet" --cookie "$cookie" *>$logFile 2>&1

if (Test-Path $logFile) {
  Write-Host "`n📄 Περιεχόμενα Log αρχείου:`n"
  Get-Content $logFile | Out-String | Write-Host
} else {
  Write-Host "❌ Το αρχείο log δεν δημιουργήθηκε."
}
