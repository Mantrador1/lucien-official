Stop-Process -Name python -ErrorAction SilentlyContinue

python -m venv venv

. .\venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install flask requests flask-cors python-dotenv

$env:OPENROUTER_API_KEY = 'YOUR_OPENROUTER_API_KEY_HERE'
$env:PORT = '5050'

Start-Process powershell -ArgumentList '-NoExit', '-Command', 'python main.py'

Start-Sleep -Seconds 10

$response = Invoke-RestMethod -Uri "http://localhost:5050/ask" 
    -Method POST 
    -Body (@{ prompt = "Hello, who are you?" } | ConvertTo-Json) 
    -ContentType "application/json"

Write-Host "Response from server:"
Write-Host $response.response

