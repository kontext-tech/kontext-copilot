# Build ui and then copy the output to kontext_copilot/ui
# And then build the kontext-copilot using poetry

# Stop execution on any error
$ErrorActionPreference = 'Stop'

# Build ui
Set-Location ./ui
Write-Output "Building ui"
npm run generate

# Ensure destination directory exists
$destinationPath = "../kontext_copilot/ui"
if (-Not (Test-Path -Path $destinationPath)) {
    New-Item -Path $destinationPath -ItemType Directory
}

# Copy .output/public to ../kontext_copilot/ui
Write-Output "Copying ui output to kontext_copilot/ui"
Copy-Item -Path .output/public/* -Destination $destinationPath -Recurse -Force

Set-Location ..

# Build kontext-copilot
Write-Output "Building kontext-copilot"
poetry build

Write-Output "Build completed"
