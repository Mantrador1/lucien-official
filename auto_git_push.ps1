while ($true) {
    try {
        git add .
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        git commit -m "?? Auto-commit at $timestamp"
        git push origin main
        Write-Host "`n? Git auto-pushed at $timestamp" -ForegroundColor Green
    }
    catch {
        Write-Host "`n?? Git auto-push failed: $_" -ForegroundColor Yellow
    }
    Start-Sleep -Seconds 600  # ???e 10 ?ept?
}

