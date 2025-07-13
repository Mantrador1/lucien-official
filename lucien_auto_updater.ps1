# Define paths
$repoPath = "C:\lucien_proxy"
$logFile = "$repoPath\logs\updater.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Set-Location $repoPath
git fetch origin
$localHash = git rev-parse HEAD
$remoteHash = git rev-parse origin/main

if ($localHash -ne $remoteHash) {
    "`n[$timestamp] 🔄 Update found. Pulling latest changes..." | Out-File -Append $logFile
    git reset --hard origin/main
    "`n[$timestamp] ✅ Update completed. Restarting Lucien..." | Out-File -Append $logFile

    Get-CimInstance Win32_Process | Where-Object {
        $_.CommandLine -like "*main.py*" -or
        $_.CommandLine -like "*telegram_listener.py*" -or
        $_.CommandLine -like "*lucien_laptop_link.ps1*"
    } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force; Start-Sleep -Milliseconds 300 }

    Start-Process "python" "main.py"
    Start-Sleep -Seconds 2
    Start-Process "python" "telegram_listener.py"
} else {
    "`n[$timestamp] ✅ Lucien is up to date. No update needed." | Out-File -Append $logFile
}
