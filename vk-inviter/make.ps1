param (
    [switch] $Init,
    [switch] $Clean,
    [switch] $Compile
)
Set-Location $PSScriptRoot
$didSomething = $false

if ($Init) {
    & py -m venv ./.venv
    . ./.venv/Scripts/Activate.ps1

    & ./.venv/Scripts/python -m pip install --upgrade pip
    & ./.venv/Scripts/python -m pip install --upgrade -r ./requirements.txt
    & ./.venv/Scripts/python -m pip install --upgrade pyinstaller
    $didSomething = $true
}

if ($Clean) {
    Remove-Item -Recurse -ErrorAction Ignore ./dist
    $didSomething = $true
}
if ($Compile) {
    & ./.venv/Scripts/pyinstaller --specpath ./build ./vk_inviter.py
    Remove-Item -Recurse -ErrorAction Ignore ./build, ./__pycache__
    Remove-Item './dist/vk_inviter/MSVCP140.dll', `
                './dist/vk_inviter/VCRUNTIME140.dll', `
                './dist/vk_inviter/api-ms-*'
    "@echo off`r`n`"%~dp0vk_inviter\vk_inviter.exe`"" | Out-File ./dist/Приглашатор.bat -Encoding Ascii
    Compress-Archive ./dist/* "./dist/vk_inviter-win64-$(Get-Date -Format 'yyMMddHHmm').zip"
    $didSomething = $true
}

if (!$didSomething) {
    Get-Help $PSCommandPath
}