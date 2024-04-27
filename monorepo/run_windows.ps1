# Step 1: Check if Node.js is installed and in the PATH
function Test-NodeInPath {
    $nodeInPath = $False
    try {
        # Attempt to execute node command
        node --version
        $nodeInPath = $True
    } catch {
        Write-Output "Node.js is installed but not found in PATH."
    }
    return $nodeInPath
}

# Check for Node.js and try to add to PATH if necessary
if (-Not (Get-Command node -ErrorAction SilentlyContinue) -or -Not (Test-NodeInPath)) {
    # Step 2: Download and install Node.js
    Write-Output "Installing Node.js..."

    # Define the Node.js version to install
    $nodeVersion = "node-v16.14.2-win-x64"
    $url = "https://nodejs.org/dist/v16.14.2/$nodeVersion.zip"

    # Specify path to save the Node.js ZIP
    $output = "$env:USERPROFILE\Downloads\$nodeVersion.zip"

    # Download Node.js
    Invoke-WebRequest -Uri $url -OutFile $output

    # Extract Node.js
    $nodeExtractPath = "$env:USERPROFILE\NodeJS"
    Expand-Archive -LiteralPath $output -DestinationPath $nodeExtractPath

    # Add Node.js to PATH
    $newPath = "$nodeExtractPath\$nodeVersion"
    $env:Path += ";$newPath"
    [Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::Machine)
    
    if (Test-NodeInPath) {
        Write-Output "Node.js installed and added to PATH successfully."
    } else {
        Write-Output "Failed to add Node.js to PATH. Please add manually to System Environment Variables."
    }
} else {
    Write-Output "Node.js is already installed and available in PATH."
}

# Step 3: Install Nx CLI globally using npm
Write-Output "Installing Nx CLI..."
npm install -g nx

Write-Output "Nx installation completed successfully. You can now start using Nx!"


nx run-many --target=serve --projects=frontend,backend --parallel
