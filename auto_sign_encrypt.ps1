$mainPath = "$PWD\main.py"
$backupPath = "$PWD\main_backup.py"
$encPath = "$PWD\main_backup.enc"
$sigPath = "$PWD\main.sig"
$secretKey = "5e3c91d2b7f849ddadf84613e06f29f1"

function Sign-And-Encrypt {
    # Δημιουργία backup
    Copy-Item $mainPath $backupPath -Force

    # Υπογραφή HMAC
    $hmac = New-Object Security.Cryptography.HMACSHA256
    $hmac.Key = [Text.Encoding]::UTF8.GetBytes($secretKey)
    $bytes = [IO.File]::ReadAllBytes($mainPath)
    $signature = ($hmac.ComputeHash($bytes) | ForEach-Object { $_.ToString("x2") }) -join ""
    Set-Content -Path $sigPath -Value $signature

    # Κρυπτογράφηση AES
    $keyBytes = [Text.Encoding]::UTF8.GetBytes($secretKey.PadRight(32,'0').Substring(0,32))
    $iv = New-Object byte[] 16
    [Security.Cryptography.RNGCryptoServiceProvider]::Create().GetBytes($iv)
    $data = [IO.File]::ReadAllBytes($backupPath)
    $aes = [Security.Cryptography.Aes]::Create()
    $aes.Mode = "CBC"
    $aes.Key = $keyBytes
    $aes.IV = $iv
    $encryptor = $aes.CreateEncryptor()
    $encrypted = $encryptor.TransformFinalBlock($data, 0, $data.Length)
    [IO.File]::WriteAllBytes($encPath, $iv + $encrypted)

    Remove-Item $backupPath -Force
    Write-Host "`n🔏 main.py υπογράφηκε και κρυπτογραφήθηκε!" -ForegroundColor Cyan
}

$lastHash = ""
while ($true) {
    if (Test-Path $mainPath) {
        $currentHash = (Get-FileHash $mainPath).Hash
        if ($currentHash -ne $lastHash) {
            $lastHash = $currentHash
            Sign-And-Encrypt
        }
    }
    Start-Sleep -Seconds 60
}

