from flask import Flask, request, jsonify
import json
import random
import time
from typing import Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class SimpleAI:
    """
    A simple AI response generator. Replace this with your preferred AI service.
    Options include: OpenAI API, Hugging Face Transformers, local models, etc.
    """
    
    def __init__(self):
        # Sample responses for demonstration
        self.response_templates = [
            "That's an interesting question about '{message}'. Let me think about that...",
            "Regarding '{message}', I would say that this is a complex topic that requires careful consideration.",
            "Thanks for asking about '{message}'. Based on my understanding, here's what I think...",
            "Your question about '{message}' brings up several important points to consider.",
            "I appreciate you sharing '{message}' with me. Here's my perspective on this matter..."
        ]
        
        self.follow_up_content = [
            "This involves multiple factors that we should consider carefully.",
            "There are several approaches we could take to address this.",
            "The key is to understand the underlying principles at work here.",
            "Let me break this down into more manageable components.",
            "This is definitely something worth exploring further."
        ]
    
    def generate_response(self, user_message: str) -> str:
        """
        Generate an AI response. Replace this method with your actual AI integration.
        
        For production use, consider integrating with:
        - OpenAI API (GPT-3.5/GPT-4)
        - Hugging Face Transformers
        - Local models like Llama, Mistral, etc.
        - Other AI services
        """
        try:
            # Simulate processing time
            time.sleep(0.5)
            
            # Simple response generation (replace with actual AI)
            template = random.choice(self.response_templates)
            follow_up = random.choice(self.follow_up_content)
            
            response = template.format(message=user_message[:50] + "..." if len(user_message) > 50 else user_message)
            response += f" {follow_up}"
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again."

# Initialize AI service
ai_service = SimpleAI()

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
    return jsonify({"status": "healthy", "service": "AI Chat Server"}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.info("Starting AI Chat Server...")
    logger.info("Server will be available at: http://localhost:5001")
    logger.info("AI Chat endpoint: http://localhost:5001/ai-chat")
    logger.info("Health check: http://localhost:5001/health")
    
    # Run the Flask server
    app.run(
        host='localhost',
        port=5001,
        debug=True,
        threaded=True
    ) 