$ErrorActionPreference = "Stop"

# ???a??asµ?? Mega.nz
$username = "fotoniomail@gmail.com"
$password = "17745167"

# F??e??? ??a backup
$localFolder = "C:\lucien_proxy"
$remoteFolder = "/lucien_backup"

# Login st? Mega
mega-login $username $password

# ??µ??????a remote fa????? a? de? ?p???e?
if (-not (mega-ls $remoteFolder 2>$null)) {
    mega-mkdir $remoteFolder
}

# S???????sµ?? a??e???
mega-put "$localFolder\*" $remoteFolder --reload

Write-Host "`n? Backup to Mega.nz completed at $(Get-Date)" -ForegroundColor Green

