param (
    [Parameter(Mandatory = $true)]
    [string]$Payload
)

$secretKey = "5e3c91d2b7f849ddadf84613e06f29f1"
$keyBytes = [System.Text.Encoding]::UTF8.GetBytes($secretKey)
$payloadBytes = [System.Text.Encoding]::UTF8.GetBytes($Payload)

$hmac = New-Object System.Security.Cryptography.HMACSHA256
$hmac.Key = $keyBytes
$signature = ($hmac.ComputeHash($payloadBytes) | ForEach-Object { $_.ToString("x2") }) -join ""

$body = @{
    payload = $Payload
    signature = $signature
} | ConvertTo-Json -Compress

$response = Invoke-RestMethod `
    -Uri "https://lucien-outside.fly.dev/control" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

Write-Host "`n🛰️ Response from Outside Lucien:`n$response.result" -ForegroundColor Cyan

