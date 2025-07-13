Start-Process powershell -ArgumentList "-NoExit", "-Command", "ollama run orca-mini" -WindowStyle Hidden
Start-Sleep -Seconds 5
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python .\app.py"

