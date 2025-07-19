# AI Chatbot Application

A real-time chatbot application built with React (frontend), C# ASP.NET Core with SignalR (backend), and Python with Ollama (AI processing).

## Architecture

```
React Frontend ←→ SignalR ←→ C# Backend ←→ Python Script ←→ Ollama AI
```

## Prerequisites

Before running this application, make sure you have the following installed:

1. **Node.js** (v16 or higher) - for React frontend
2. **.NET 9 SDK** - for C# backend
3. **Python 3.8+** - for AI processing script
4. **Ollama** - for AI model hosting

## Setup Instructions

### 1. Install Ollama

First, install Ollama from [https://ollama.ai](https://ollama.ai)

Then pull a model (e.g., llama2):
```bash
ollama pull llama2
```

Start Ollama service:
```bash
ollama serve
```

### 2. Setup Python Dependencies

Navigate to the Python AI directory and install dependencies:
```bash
cd python-ai
pip install -r requirements.txt
```

### 3. Setup C# Backend

Navigate to the backend directory:
```bash
cd backend/ChatBotApi
```

Restore packages:
```bash
dotnet restore
```

Build the project:
```bash
dotnet build
```

### 4. Setup React Frontend

Navigate to the frontend directory:
```bash
cd frontend/chatbot-ui
```

Install dependencies:
```bash
npm install
```

## Running the Application

### Step 1: Start Ollama (if not already running)
```bash
ollama serve
```

### Step 2: Start the C# Backend
```bash
cd backend/ChatBotApi
dotnet run
```
The backend will start on `https://localhost:7020`

### Step 3: Start the React Frontend
```bash
cd frontend/chatbot-ui
npm start
```
The frontend will start on `http://localhost:3000`

### Step 4: Open your browser
Navigate to `http://localhost:3000` and start chatting with the AI!

## Configuration

### Python AI Configuration
Edit `python-ai/config.py` to change:
- Ollama model (default: llama2)
- Ollama URL (default: http://localhost:11434)
- Request timeout

### C# Backend Configuration
Edit `backend/ChatBotApi/appsettings.json` to change:
- Python script path
- Python executable path

### React Frontend Configuration
Edit the SignalR connection URL in `frontend/chatbot-ui/src/App.js` if your backend runs on a different port.

## Project Structure

```
llm/
├── backend/
│   └── ChatBotApi/
│       ├── Hubs/
│       │   └── ChatHub.cs          # SignalR hub for real-time communication
│       ├── Services/
│       │   ├── IPythonAiService.cs # Service interface
│       │   └── PythonAiService.cs  # Python script execution service
│       ├── Program.cs              # Application configuration
│       └── appsettings.json        # Configuration settings
├── frontend/
│   └── chatbot-ui/
│       ├── src/
│       │   ├── App.js              # Main React component
│       │   └── App.css             # Styles
│       └── package.json            # Dependencies
├── python-ai/
│   ├── ai_chat.py                  # Main Python script
│   ├── config.py                   # Configuration
│   └── requirements.txt            # Python dependencies
└── README.md                       # This file
```

## Features

- **Real-time messaging** using SignalR
- **Beautiful chat interface** with typing indicators
- **Error handling** and connection status
- **Mobile responsive** design
- **Configurable AI models** through Ollama
- **Cross-platform** support

## Troubleshooting

### Common Issues

1. **"Could not connect to Ollama"**
   - Make sure Ollama is running: `ollama serve`
   - Check if the model is installed: `ollama list`

2. **SignalR connection failed**
   - Ensure the C# backend is running
   - Check the backend URL in the React app
   - Verify CORS settings

3. **Python script errors**
   - Check Python dependencies: `pip install -r requirements.txt`
   - Verify Python executable path in appsettings.json

### Backend URL Configuration

If you're running the backend on a different port, update the SignalR connection URL in `frontend/chatbot-ui/src/App.js`:

```javascript
const newConnection = new signalR.HubConnectionBuilder()
  .withUrl('https://localhost:YOUR_PORT/chatHub') // Update this URL
  .withAutomaticReconnect()
  .build();
```

## Available Ollama Models

Some popular models you can use:
- `llama2` - General purpose (7B, 13B, 70B variants)
- `codellama` - Code-focused
- `mistral` - High performance
- `llama2-uncensored` - Uncensored variant
- `neural-chat` - Conversational AI

Install a model with: `ollama pull model-name`

## Development

### Adding New Features

1. **Backend**: Add new methods to `ChatHub.cs` or create new services
2. **Frontend**: Modify `App.js` and `App.css` for UI changes
3. **Python AI**: Extend `ai_chat.py` for custom AI processing

### Security Notes

- The application runs locally by default
- For production deployment, implement proper authentication
- Consider rate limiting for API calls
- Secure the Python script execution

## License

This project is for educational and development purposes. 