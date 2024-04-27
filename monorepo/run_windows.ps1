# Function to test if Node.js is available in PATH
function Test-NodeInPath {
    try {
        $nodeVersion = node --version
        Write-Output "Node.js is installed with version $nodeVersion."
        return $true
    } catch {
        Write-Output "Node.js is not found in PATH."
        return $false
    }
}

# Function to fetch the latest LTS version of Node.js
function Get-LatestNodeLTSVersion {
    $nodeDistUrl = "https://nodejs.org/dist/index.json"
    $nodeVersions = Invoke-RestMethod -Uri $nodeDistUrl
    $latestLTS = $nodeVersions | Where-Object { $_.lts -ne $false } | Sort-Object version -Descending | Select-Object -First 1
    return $latestLTS
}

# Set execution policy to allow scripts to run
Set-ExecutionPolicy Bypass -Scope Process -Force

# Check if nvm is installed, if not download and install nvm-windows
$nvmDir = "$ENV:APPDATA\nvm"
if (-Not (Test-Path $nvmDir)) {
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
}

# Load nvm to use in the current session
& "$nvmDir\nvm.exe"

# Install the latest LTS version of Node.js
nvm install lts

# Use the latest LTS version
nvm use lts

# Install or upgrade Node.js if not the latest LTS
$latestLTS = Get-LatestNodeLTSVersion
if (-Not (Get-Command node -ErrorAction SilentlyContinue) -or -Not (Test-NodeInPath)) {
    Write-Output "Node.js is not the latest LTS or not found in PATH. Installing/upgrading..."
    
    $nodeVersion = $latestLTS.version -replace "v", ""
    $nodeLTSFileName = "node-$nodeVersion-win-x64"
    $url = "https://nodejs.org/dist/$latestLTS.version/$nodeLTSFileName.zip"

    $output = "$env:USERPROFILE\Downloads\$nodeLTSFileName.zip"
    Invoke-WebRequest -Uri $url -OutFile $output

    $nodeExtractPath = "$env:USERPROFILE\NodeJS"
    Expand-Archive -LiteralPath $output -DestinationPath $nodeExtractPath -Force

    $newPath = "$nodeExtractPath\$nodeLTSFileName"
    $env:Path += ";$newPath"
    [Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::Machine)

    if (Test-NodeInPath) {
        Write-Output "Node.js upgraded/installed to latest LTS version successfully."
    } else {
        Write-Output "Failed to add Node.js to PATH. Please add manually to System Environment Variables."
    }
} else {
    Write-Output "Node.js is already installed with the latest LTS version."
}

# Step 3: Install Nx CLI globally using npm
Write-Output "Installing Nx CLI..."
npm install -g nx

Write-Output "Nx installation completed successfully. You can now start using Nx!"


nx run-many --target=serve --projects=frontend,backend --parallel
