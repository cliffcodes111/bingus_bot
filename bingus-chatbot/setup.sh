#!/bin/bash

# AI Chatbot Setup Script for Linux/Mac
echo -e "\033[32m=== AI Chatbot Application Setup ===\033[0m"

# Check if required tools are installed
echo -e "\033[33mChecking prerequisites...\033[0m"

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "\033[32m✓ Node.js found: $NODE_VERSION\033[0m"
else
    echo -e "\033[31m✗ Node.js not found. Please install Node.js from https://nodejs.org/\033[0m"
    exit 1
fi

# Check .NET
if command -v dotnet &> /dev/null; then
    DOTNET_VERSION=$(dotnet --version)
    echo -e "\033[32m✓ .NET found: $DOTNET_VERSION\033[0m"
else
    echo -e "\033[31m✗ .NET not found. Please install .NET 9 SDK from https://dotnet.microsoft.com/\033[0m"
    exit 1
fi

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "\033[32m✓ Python found: $PYTHON_VERSION\033[0m"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo -e "\033[32m✓ Python found: $PYTHON_VERSION\033[0m"
    PYTHON_CMD="python"
else
    echo -e "\033[31m✗ Python not found. Please install Python from https://python.org/\033[0m"
    exit 1
fi

echo -e "\n\033[32m=== Setting up Python Dependencies ===\033[0m"
cd python-ai
$PYTHON_CMD -m pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "\033[32m✓ Python dependencies installed\033[0m"
else
    echo -e "\033[31m✗ Failed to install Python dependencies\033[0m"
    exit 1
fi
cd ..

echo -e "\n\033[32m=== Setting up .NET Backend ===\033[0m"
cd backend/ChatBotApi
dotnet restore
dotnet build
if [ $? -eq 0 ]; then
    echo -e "\033[32m✓ .NET backend built successfully\033[0m"
else
    echo -e "\033[31m✗ Failed to build .NET backend\033[0m"
    exit 1
fi
cd ../..

echo -e "\n\033[32m=== Setting up React Frontend ===\033[0m"
cd frontend/chatbot-ui
npm install
if [ $? -eq 0 ]; then
    echo -e "\033[32m✓ React dependencies installed\033[0m"
else
    echo -e "\033[31m✗ Failed to install React dependencies\033[0m"
    exit 1
fi
cd ../..

echo -e "\n\033[32m=== Setup Complete! ===\033[0m"
echo -e "\033[33mNext steps:\033[0m"
echo -e "\033[37m1. Install Ollama from https://ollama.ai\033[0m"
echo -e "\033[37m2. Run: ollama pull llama2\033[0m"
echo -e "\033[37m3. Run: ollama serve\033[0m"
echo -e "\033[37m4. In a new terminal, run the backend: cd backend/ChatBotApi && dotnet run\033[0m"
echo -e "\033[37m5. In another terminal, run the frontend: cd frontend/chatbot-ui && npm start\033[0m"
echo -e "\033[37m6. Open http://localhost:3000 in your browser\033[0m"

echo -e "\n\033[36mFor detailed instructions, see README.md\033[0m" 