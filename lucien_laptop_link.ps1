$uri = 'http://127.0.0.1:5000/ask'
$headers = @{ 'Content-Type' = 'application/json' }
$body = @{ question = 'ping from laptop link' } | ConvertTo-Json -Compress

try {
    $response = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body -TimeoutSec 5
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - Response: $($response.response)" | Add-Content -Path "C:\lucien_proxy\logs\laptop_link.log"
} catch {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - ERROR: $_" | Add-Content -Path "C:\lucien_proxy\logs\laptop_link.log"
}
