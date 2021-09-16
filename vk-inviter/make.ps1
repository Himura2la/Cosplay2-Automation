param (
    [switch] $InstallRequirements,
    [switch] $InstallPyInstaller,
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
if ($Compile) {
    & py -m PyInstaller --onefile --specpath ./build ./vk_inviter.py
    Remove-Item -Recurse ./build, ./__pycache__
    $didSomething = $true
}

if (!$didSomething) {
    Get-Help $PSCommandPath
}