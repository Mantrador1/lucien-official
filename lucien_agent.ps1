# lucien_agent.ps1 - Interactive local chat with Lucien via OpenRouter (Claude 3 Opus)

$utf8NoBom = New-Object System.Text.UTF8Encoding $false

while ($true) {
    $prompt = Read-Host "`nðŸ§  Î•ÏÏŽÏ„Î·ÏƒÎ· Ï€ÏÎ¿Ï‚ Lucien"
    if ($prompt -in @("exit", "quit", "Î¾Î­Î¾Î¹Ï„")) { break }

    $body = @{
        model = "anthropic/claude-3-opus:beta"
        prompt = $prompt
    } | ConvertTo-Json -Depth 3

    $bodyBytes = $utf8NoBom.GetBytes($body)

    try {
        $response = Invoke-RestMethod -Uri "http://127.0.0.1:5050/ask" `
                    -Method POST `
                    -ContentType "application/json" `
                    -Body $bodyBytes
        "`nLucien: $($response.response)"
    } catch {
        Write-Host "`nâŒ Î£Ï†Î¬Î»Î¼Î±: $_" -ForegroundColor Red
    }
}

