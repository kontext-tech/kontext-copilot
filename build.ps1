# Build client-app and then copy the output to kontext_ai/client-app
# And then build the kontext-ai using poetry

# Stop execution on any error
$ErrorActionPreference = 'Stop'

# Build client-app
Set-Location .\client-app
Write-Output "Building client-app"
npm run generate

# Copy .output/public to ../kontext_ai/client-app
Write-Output "Copying client-app output to kontext_ai/client-app"
Copy-Item -Path .output\public\* -Destination ..\kontext_ai\client-app\ -Recurse -Force

Set-Location ..

# Build kontext-ai
Write-Output "Building kontext-ai"
poetry build

Write-Output "Build completed"
