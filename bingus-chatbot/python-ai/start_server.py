#!/usr/bin/env python3
"""
AI Server Startup Script
Provides options to start either the basic AI server or OpenAI-enabled server.
"""

import sys
import os
import subprocess
import argparse

def check_requirements():
    """Check if required packages are installed."""
    try:
        import flask
        import requests
        print("✓ Required packages found")
        return True
    except ImportError as e:
        print(f"✗ Missing required packages: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_openai():
    """Check if OpenAI package and API key are available."""
    try:
        import openai
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            print("✓ OpenAI package and API key found")
            return True
        else:
            print("⚠ OpenAI package found but no API key set")
            return False
    except ImportError:
        print("⚠ OpenAI package not installed")
        return False

def main():
    parser = argparse.ArgumentParser(description='Start the AI Chat Server')
    parser.add_argument(
        '--mode', 
        choices=['basic', 'openai', 'auto'], 
        default='auto',
        help='Server mode: basic (simple responses), openai (GPT), or auto (detect best option)'
    )
    parser.add_argument(
        '--port', 
        type=int, 
        default=5001,
        help='Port to run the server on (default: 5001)'
    )
    
    args = parser.parse_args()
    
    print("🤖 AI Chat Server Startup")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Determine which server to run
    server_script = None
    
    if args.mode == 'basic':
        server_script = 'ai_server.py'
        print("📋 Starting basic AI server...")
    elif args.mode == 'openai':
        if check_openai():
            server_script = 'ai_server_openai.py'
            print("🚀 Starting OpenAI-enabled server...")
        else:
            print("❌ OpenAI mode requested but requirements not met")
            sys.exit(1)
    else:  # auto mode
        if check_openai():
            server_script = 'ai_server_openai.py'
            print("🚀 Auto-detected: Starting OpenAI-enabled server...")
        else:
            server_script = 'ai_server.py'
            print("📋 Auto-detected: Starting basic AI server...")
    
    print(f"🌐 Server will be available at: http://localhost:{args.port}")
    print("📡 AI Chat endpoint: /ai-chat")
    print("❤️ Health check: /health")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 40)
    
    try:
        # Set port environment variable if different from default
        env = os.environ.copy()
        if args.port != 5001:
            env['PORT'] = str(args.port)
        
        # Run the selected server
        subprocess.run([sys.executable, server_script], env=env)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 