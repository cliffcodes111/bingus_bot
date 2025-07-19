# AI Chatbot Setup Script for Windows
Write-Host "=== AI Chatbot Application Setup ===" -ForegroundColor Green

# Check if required tools are installed
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check Node.js
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found. Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Check .NET
try {
    $dotnetVersion = dotnet --version
    Write-Host "✓ .NET found: $dotnetVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ .NET not found. Please install .NET 9 SDK from https://dotnet.microsoft.com/" -ForegroundColor Red
    exit 1
}

# Check Python
try {
    $pythonVersion = python --version
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python from https://python.org/" -ForegroundColor Red
    exit 1
}

Write-Host "`n=== Setting up Python Dependencies ===" -ForegroundColor Green
Set-Location "python-ai"
python -m pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install Python dependencies" -ForegroundColor Red
    exit 1
}
Set-Location ".."

Write-Host "`n=== Setting up .NET Backend ===" -ForegroundColor Green
Set-Location "backend/ChatBotApi"
dotnet restore
dotnet build
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ .NET backend built successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to build .NET backend" -ForegroundColor Red
    exit 1
}
Set-Location "../.."

Write-Host "`n=== Setting up React Frontend ===" -ForegroundColor Green
Set-Location "frontend/chatbot-ui"
npm install
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ React dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install React dependencies" -ForegroundColor Red
    exit 1
}
Set-Location "../.."

Write-Host "`n=== Setup Complete! ===" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Install Ollama from https://ollama.ai" -ForegroundColor White
Write-Host "2. Run: ollama pull llama2" -ForegroundColor White
Write-Host "3. Run: ollama serve" -ForegroundColor White
Write-Host "4. In a new terminal, run the backend: cd backend/ChatBotApi && dotnet run" -ForegroundColor White
Write-Host "5. In another terminal, run the frontend: cd frontend/chatbot-ui && npm start" -ForegroundColor White
Write-Host "6. Open http://localhost:3000 in your browser" -ForegroundColor White

Write-Host "`nFor detailed instructions, see README.md" -ForegroundColor Cyan 