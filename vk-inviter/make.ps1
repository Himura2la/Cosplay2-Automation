param (
    [switch] $InstallRequirements,
    [switch] $InstallPyInstaller,
    [switch] $Clean,
    [switch] $Compile
)
Set-Location $PSScriptRoot
$didSomething = $false

if ($InstallRequirements -or $InstallPyInstaller) {
    & py -m pip install --user --upgrade pip
}
if ($InstallRequirements) {
    & py -m pip install --user --upgrade -r ./requirements.txt
    # The 'python3-tk' package is also required on Linux.
    $didSomething = $true
}
if ($InstallPyInstaller) {
    & py -m pip install --user --upgrade pyinstaller
    $didSomething = $true
}
if ($Clean) {
    Remove-Item -Recurse -Force ./dist
    $didSomething = $true
}
if ($Compile) {
    & py -m PyInstaller --specpath ./build ./vk_inviter.py
    Remove-Item -Recurse -Force ./build, ./__pycache__
    "@echo off`r`n`"%~dp0vk_inviter\vk_inviter.exe`"" | Out-File "./dist/Приглашатор.bat" -Encoding Ascii
    $didSomething = $true
}

if (!$didSomething) {
    Get-Help $PSCommandPath
}