Clear-Host
$logFile = "C:\lucien_proxy\execution_status_log.txt"

if (-not (Test-Path $logFile)) {
    Write-Host "❌ Δεν βρέθηκε log αρχείο στο $logFile"
    exit
}

Write-Host "`n📊 LIVE DASHBOARD - GALXE FARMING STATUS" -ForegroundColor Cyan

while ($true) {
    Clear-Host
    Write-Host "`n🔄 Ανανεώνεται κάθε 10 δευτερόλεπτα..." -ForegroundColor DarkGray
    Write-Host "`n📊 GALXE FARMING DASHBOARD" -ForegroundColor Green
    Write-Host "============================="

    Get-Content $logFile |
    ForEach-Object {
        $parts = $_ -split "\s+"
        [PSCustomObject]@{
            Wallet = $parts[0]
            Status = $parts[1]
            Time   = $parts[2..($parts.Count - 1)] -join " "
        }
    } |
    Group-Object Wallet |
    ForEach-Object {
        $wallet = $_.Name
        $success = ($_.Group | Where-Object { $_.Status -eq "OK" }).Count
        $fail = ($_.Group | Where-Object { $_.Status -eq "FAIL" }).Count
        $lastTime = ($_.Group | Sort-Object Time -Descending | Select-Object -First 1).Time
        [PSCustomObject]@{
            Wallet = $wallet
            Success = $success
            Fail = $fail
            "Last Run" = $lastTime
        }
    } |
    Format-Table -AutoSize

    Start-Sleep -Seconds 10
}
