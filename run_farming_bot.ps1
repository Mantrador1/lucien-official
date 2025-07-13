# PowerShell script to run Python bot with automatic loading of wallets and proxies

# Ορίστε τα paths των αρχείων wallets και proxies
 = '.\wallets.enc'
 = '.\wallet_key.key'
 = '.\proxies.txt'  # Δημιούργησε ένα αρχείο με proxies, ένα ανά γραμμή

# Έλεγχος ύπαρξης αρχείων
if (-Not (Test-Path )) { Write-Error "Missing wallets.enc file!"; exit }
if (-Not (Test-Path )) { Write-Error "Missing wallet_key.key file!"; exit }
if (-Not (Test-Path )) { Write-Warning "Proxies file not found, proceeding without proxies." }

# Διάβασε proxies σε λίστα
 = @()
if (Test-Path ) {
     = Get-Content  | Where-Object { .Trim() -ne '' }
}

# Δημιουργία αρχείου proxies_list.py για το Python script
 = "PROXIES = ["
foreach ( in ) {
     += ""","
}
 = .TrimEnd(',') + "]
"
Set-Content -Encoding UTF8 -Path '.\proxies_list.py' -Value 

# Τρέξε το Python bot
python .\bot_with_wallets.py

