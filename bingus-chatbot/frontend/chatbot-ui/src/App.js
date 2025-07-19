import React, { useState, useEffect, useRef } from 'react';
import * as signalR from '@microsoft/signalr';
import './App.css';

function App() {
  const [connection, setConnection] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Create SignalR connection
    const newConnection = new signalR.HubConnectionBuilder()
      .withUrl('https://localhost:7213/chatHub') // Update this to match your backend URL
      .withAutomaticReconnect()
      .build();

    setConnection(newConnection);

    return () => {
      if (newConnection) {
        newConnection.stop();
      }
    };
  }, []);

  useEffect(() => {
    if (connection) {
      connection.start()
        .then(() => {
          console.log('Connected to SignalR');
          setIsConnected(true);

          // Listen for messages
          connection.on('ReceiveMessage', (sender, message) => {
            const newMessage = {
              id: Date.now() + Math.random(),
              sender: sender,
              message: message,
              timestamp: new Date()
            };
            setMessages(prevMessages => [...prevMessages, newMessage]);
            
            if (sender === 'AI') {
              setIsLoading(false);
            }
          });
        })
        .catch(err => {
          console.error('Connection failed: ', err);
          setIsConnected(false);
        });

      connection.onclose(() => {
        setIsConnected(false);
        setIsLoading(false);
      });

      connection.onreconnected(() => {
        setIsConnected(true);
      });
    }
  }, [connection]);

  const sendMessage = async () => {
    if (inputMessage.trim() && connection && isConnected) {
      setIsLoading(true);
      try {
        await connection.invoke('SendMessage', inputMessage);
        setInputMessage('');
      } catch (err) {
        console.error('Error sending message: ', err);
        setIsLoading(false);
        // Add error message to chat
        const errorMessage = {
          id: Date.now(),
          sender: 'System',
          message: 'Failed to send message. Please try again.',
          timestamp: new Date()
        };
        setMessages(prevMessages => [...prevMessages, errorMessage]);
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="App">
      <header className="chat-header">
        <h1>AI Chatbot</h1>
        <div className="connection-status">
          <span className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}></span>
          {isConnected ? 'Connected' : 'Disconnected'}
          <button onClick={clearChat} className="clear-button">Clear Chat</button>
        </div>
      </header>

      <div className="chat-container">
        <div className="messages-container">
          {messages.length === 0 && (
            <div className="welcome-message">
              <p>Welcome to the AI Chatbot! Type a message to start the conversation.</p>
              <p><strong>Note:</strong> Make sure Ollama is running and you have a model installed (e.g., llama2).</p>
            </div>
          )}
          
          {messages.map((message) => (
            <div key={message.id} className={`message ${message.sender.toLowerCase()}`}>
              <div className="message-header">
                <strong>{message.sender}</strong>
                <span className="timestamp">
                  {message.timestamp.toLocaleTimeString()}
                </span>
              </div>
              <div className="message-content">{message.message}</div>
            </div>
          ))}
          
          {isLoading && (
            <div className="message ai">
              <div className="message-header">
                <strong>AI</strong>
              </div>
              <div className="message-content loading">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                Thinking...
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        <div className="input-container">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here..."
            disabled={!isConnected || isLoading}
            rows="3"
          />
          <button 
            onClick={sendMessage} 
            disabled={!isConnected || isLoading || !inputMessage.trim()}
            className="send-button"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
