if (!(Test-Path ".\logs")) {
    New-Item -Path ".\logs" -ItemType Directory | Out-Null
}

$agents = @("start_helper.ps1", "start_watchdog.ps1", "start_stealth.ps1")

foreach ($agent in $agents) {
    $fullPath = Join-Path $PWD $agent
    if (Test-Path $fullPath) {
        Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File `"$fullPath`"" -WindowStyle Hidden
        Write-Host "`n✅ Started: $agent" -ForegroundColor Green
    } else {
        Write-Host "`n❌ Missing script: $agent" -ForegroundColor Red
    }
}

