while (True) {
    try {
        \ = Get-ChildItem -Recurse -Include *.py,*.log -Path .\lucien_proxy | Get-Content -ErrorAction SilentlyContinue | Select-String -Pattern 'Exception|Traceback|Error|FAIL|invalid|not defined'
        if (\) {
            \ = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
            Add-Content -Path .\error_log.txt -Value "
[\] ?? Detected issue:
\"
            Write-Host "
?? Error detected and logged at \" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "
? Scanner error: \"
    }
    Start-Sleep -Seconds 300  # ???e 5 ?ept?
}

