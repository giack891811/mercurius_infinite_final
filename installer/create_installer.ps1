$solution = Join-Path $PSScriptRoot 'MercuriusInstaller.sln'

$msbuild = "${Env:ProgramFiles(x86)}\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe"
if (!(Test-Path $msbuild)) {
    $msbuild = "${Env:ProgramFiles(x86)}\Microsoft Visual Studio\2019\BuildTools\MSBuild\Current\Bin\MSBuild.exe"
}

Write-Host "Building installer via MSBuild: $solution"
& $msbuild $solution /p:Configuration=Release
