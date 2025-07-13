param (
    [string]$question
)

$jsonBody = @{ prompt = $question } | ConvertTo-Json -Depth 3

$response = Invoke-RestMethod `
    -Uri "http://127.0.0.1:5050/ask" `
    -Method POST `
    -Body $jsonBody `
    -ContentType "application/json"

Write-Host "`n🤖 AI Response:`n$response.response"

