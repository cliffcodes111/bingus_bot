from flask import Flask, request, jsonify
import os
import logging
from typing import Optional
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class OpenAIService:
    """
    OpenAI integration for generating AI responses.
    Requires OPENAI_API_KEY environment variable to be set.
    """
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = None
        
        if self.api_key:
            try:
                # Import openai only if API key is available
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
                logger.info("OpenAI client initialized successfully")
            except ImportError:
                logger.warning("OpenAI package not installed. Install with: pip install openai")
            except Exception as e:
                logger.error(f"Error initializing OpenAI client: {e}")
        else:
            logger.warning("OPENAI_API_KEY not found. Using fallback responses.")
    
    def generate_response(self, user_message: str) -> str:
        """
        Generate AI response using OpenAI API or fallback to simple responses.
        """
        if self.client and self.api_key:
            return self._generate_openai_response(user_message)
        else:
            return self._generate_fallback_response(user_message)
    
    def _generate_openai_response(self, user_message: str) -> str:
        """Generate response using OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # or "gpt-4" if you have access
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful assistant. Provide clear, concise, and friendly responses."
                    },
                    {
                        "role": "user", 
                        "content": user_message
                    }
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return self._generate_fallback_response(user_message)
    
    def _generate_fallback_response(self, user_message: str) -> str:
        """Generate fallback response when OpenAI is not available."""
        import random
        
        templates = [
            f"Thanks for your message about '{user_message[:30]}{'...' if len(user_message) > 30 else ''}'. I understand you're looking for information on this topic.",
            f"That's an interesting point about '{user_message[:30]}{'...' if len(user_message) > 30 else ''}'. Let me provide some thoughts on this.",
            f"I appreciate your question regarding '{user_message[:30]}{'...' if len(user_message) > 30 else ''}'. Here's what I can tell you about this subject.",
        ]
        
        follow_ups = [
            "While I don't have access to my full AI capabilities right now, I'd be happy to help with basic information.",
            "For more detailed responses, please ensure the AI service is properly configured.",
            "This is a basic response - full AI capabilities require proper API configuration."
        ]
        
        response = random.choice(templates) + " " + random.choice(follow_ups)
        return response

# Initialize AI service
ai_service = OpenAIService()

@app.route('/ai-chat', methods=['POST'])
def ai_chat():
    """
    AI chat endpoint that matches the C# service expectations.
    Accepts POST requests with JSON body containing 'message' field.
    """
    try:
        # Get the request data
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' field in request"}), 400
        
        user_message = data['message']
        if not user_message or not user_message.strip():
            return jsonify({"error": "Message cannot be empty"}), 400
        
        logger.info(f"Received message: {user_message}")
        
        # Generate AI response
        ai_response = ai_service.generate_response(user_message.strip())
        
        logger.info(f"Generated response: {ai_response}")
        
        # Return the response as plain text (matching C# expectations)
        return ai_response, 200, {'Content-Type': 'text/plain'}
        
    except Exception as e:
        logger.error(f"Error in ai_chat endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    api_status = "OpenAI API configured" if ai_service.api_key else "Using fallback responses"
    return jsonify({
        "status": "healthy", 
        "service": "AI Chat Server (OpenAI Edition)",
        "ai_status": api_status
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.info("Starting AI Chat Server (OpenAI Edition)...")
    logger.info("Server will be available at: http://localhost:5001")
    logger.info("AI Chat endpoint: http://localhost:5001/ai-chat")
    logger.info("Health check: http://localhost:5001/health")
    
    # Check API key status
    if ai_service.api_key:
        logger.info("✓ OpenAI API key found - using GPT responses")
    else:
        logger.warning("⚠ No OpenAI API key - using fallback responses")
        logger.info("To use OpenAI: Set OPENAI_API_KEY environment variable")
    
    # Run the Flask server
    app.run(
        host='localhost',
        port=5001,
        debug=True,
        threaded=True
    ) 