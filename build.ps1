# Build ui and then copy the output to kontext_ai/ui
# And then build the kontext-ai using poetry

# Stop execution on any error
$ErrorActionPreference = 'Stop'

# Build ui
Set-Location .\ui
Write-Output "Building ui"
npm run generate

# Copy .output/public to ../kontext_ai/ui
Write-Output "Copying ui output to kontext_ai/ui"
Copy-Item -Path .output\public\* -Destination ..\kontext_ai\ui\ -Recurse -Force

Set-Location ..

# Build kontext-ai
Write-Output "Building kontext-ai"
poetry build

Write-Output "Build completed"
