# Set execution policy to allow scripts to run
Set-ExecutionPolicy Bypass -Scope Process -Force

# Define the directory for nvm
$nvmDir = "$ENV:APPDATA\nvm"
$nvmExec = "$nvmDir\nvm.exe"

# Check if nvm is installed, if not download and install nvm-windows
if (-Not (Test-Path $nvmExec)) {
    Write-Output "nvm-windows not found. Installing..."
    # Download nvm-windows installer
    $nvmInstaller = "https://github.com/coreybutler/nvm-windows/releases/download/1.1.10/nvm-setup.zip"
    $outZip = "$ENV:TEMP\nvm-setup.zip"
    Invoke-WebRequest -Uri $nvmInstaller -OutFile $outZip

    # Extract the installer
    Expand-Archive -LiteralPath $outZip -DestinationPath $ENV:TEMP -Force

    # Run the installer
    $installer = Get-ChildItem "$ENV:TEMP" -Filter "nvm-setup.exe"
    Start-Process -FilePath $installer.FullName -Wait

    # Refresh environment variables by updating the PATH in the current session
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
}

# Ensure nvm command is recognized in the current session
if (!(Get-Command "nvm" -ErrorAction SilentlyContinue)) {
    $scriptBlock = [ScriptBlock]::Create(". $nvmExec")
    Invoke-Command -ScriptBlock $scriptBlock
}

# Install the latest LTS version of Node.js
& $nvmExec install lts

# Use the latest LTS version
& $nvmExec use lts


nx run-many --target=serve --projects=frontend,backend --parallel
