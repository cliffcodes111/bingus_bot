# Python AI Service

This directory contains the Python AI service that provides AI-generated responses for the Bingus Chatbot. The service communicates with the C# backend via HTTP requests.

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Server** (Auto-detect mode)
   ```bash
   python start_server.py
   ```

3. **Test the Connection**
   - The server will run on `http://localhost:5001`
   - Health check: `http://localhost:5001/health`
   - Your C# `GetAiResponseAsync` method should now work!

## 📁 Files Overview

- **`ai_server.py`** - Basic AI server with simple response generation
- **`ai_server_openai.py`** - Enhanced server with OpenAI GPT integration
- **`start_server.py`** - Smart startup script with auto-detection
- **`ai_chat_client.py`** - Test client for the AI service
- **`requirements.txt`** - Python dependencies
- **`README.md`** - This file

## 🛠️ Server Modes

### Basic Mode (Default fallback)
- Uses predefined response templates
- No API keys required
- Good for testing and development

### OpenAI Mode (Recommended for production)
- Uses GPT-3.5-turbo or GPT-4
- Requires OpenAI API key
- Provides intelligent, context-aware responses

## 🔧 Setup Options

### Option 1: Basic Setup (No AI API)
```bash
# Install basic requirements
pip install flask requests

# Start basic server
python ai_server.py
```

### Option 2: OpenAI Setup (Recommended)
```bash
# Install requirements including OpenAI
pip install -r requirements.txt
pip install openai

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Start OpenAI-enabled server
python ai_server_openai.py
```

### Option 3: Smart Startup (Auto-detects best option)
```bash
# Install requirements
pip install -r requirements.txt

# Start with auto-detection
python start_server.py

# Or specify mode explicitly
python start_server.py --mode openai
python start_server.py --mode basic
```

## 🔑 OpenAI API Key Setup

### Windows (PowerShell)
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

### Windows (Command Prompt)
```cmd
set OPENAI_API_KEY=your-api-key-here
```

### macOS/Linux
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Permanent Setup
Add to your system environment variables or create a `.env` file (requires python-dotenv).

## 🧪 Testing the Service

### Test with the included client
```bash
python ai_chat_client.py
```

### Test with curl
```bash
# Health check
curl http://localhost:5001/health

# AI chat request
curl -X POST http://localhost:5001/ai-chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

### Test with your C# application
Your existing `GetAiResponseAsync` method should work automatically once the Python server is running.

## 🔄 Integration with C# Backend

Your C# service (`PythonAiService.cs`) is already configured to work with this Python server:

1. **Endpoint**: `http://localhost:5001/ai-chat`
2. **Method**: POST
3. **Request**: JSON with `{"message": "user message"}`
4. **Response**: Plain text AI response

The Python server matches these exact requirements.

## 📊 API Endpoints

### POST /ai-chat
**Request:**
```json
{
  "message": "Your question here"
}
```

**Response:**
```
AI-generated response text
```

### GET /health
**Response:**
```json
{
  "status": "healthy",
  "service": "AI Chat Server",
  "ai_status": "OpenAI API configured" // or "Using fallback responses"
}
```

## 🔧 Customization

### Adding New AI Services

You can easily add support for other AI services by modifying the server scripts:

1. **Hugging Face Transformers**
2. **Anthropic Claude**
3. **Local models (Ollama, etc.)**
4. **Azure OpenAI**
5. **Google PaLM**

### Example: Adding Hugging Face
```python
from transformers import pipeline

class HuggingFaceService:
    def __init__(self):
        self.generator = pipeline('text-generation', model='gpt2')
    
    def generate_response(self, user_message):
        result = self.generator(user_message, max_length=100)
        return result[0]['generated_text']
```

## 🐛 Troubleshooting

### Common Issues

1. **Port 5001 already in use**
   ```bash
   python start_server.py --port 5002
   ```

2. **OpenAI API key not working**
   - Verify your API key is correct
   - Check your OpenAI account has credits
   - Ensure the key has proper permissions

3. **Package installation issues**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

4. **C# service can't connect**
   - Ensure Python server is running
   - Check firewall settings
   - Verify the port (5001) is accessible

### Logs and Debugging

The server provides detailed logging. Check the console output for:
- Request/response details
- Error messages
- API key status
- Connection issues

## 🚀 Production Deployment

For production use:

1. **Use a production WSGI server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5001 ai_server_openai:app
   ```

2. **Set up environment variables properly**
3. **Configure proper logging**
4. **Add rate limiting and security**
5. **Monitor API usage and costs**

## 💡 Performance Tips

1. **Use threading** - Both servers are configured with `threaded=True`
2. **Connection pooling** - Consider using connection pools for external APIs
3. **Caching** - Cache frequent responses to reduce API calls
4. **Rate limiting** - Implement rate limiting for production use

## 📋 Next Steps

1. Test the basic server with your C# application
2. Set up OpenAI API key for intelligent responses
3. Customize the AI prompts and responses for your use case
4. Add any additional AI services you need
5. Deploy to production when ready

## 🤝 Contributing

Feel free to extend this service with additional AI providers or features! 