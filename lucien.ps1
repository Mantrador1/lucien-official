Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File C:\lucien_proxy\start_local_ai.ps1"
Start-Sleep -Seconds 2
while ($true) {
    $question = Read-Host "📝 Ρώτα κάτι (ή γράψε exit για έξοδο)"
    if ($question -eq "exit") { break }

    $jsonBody = @{ prompt = $question } | ConvertTo-Json -Depth 3
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:5050/ask" -Method POST -Body $jsonBody -ContentType "application/json"

    Write-Host "`n🤖 AI Response:`n$($response.response)`n"
}

