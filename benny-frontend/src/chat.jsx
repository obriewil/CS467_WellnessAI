import React, { useState, useEffect } from 'react';
import axios from 'axios';
// import { useSession } from './contexts/SessionContext'; // JWT Token for remembering users
import ChatBubble from './components/ChatBubble';
import ChatInput from './components/ChatInput';
import Header from './components/Header';
import bennyIcon from './assets/benny_icon.png';

// API URL from env
const API_URL = import.meta.env.VITE_API_URL;

function Chat() {
  const [messages, setMessages] = useState(() => {
    const pendingMessage = sessionStorage.getItem('pendingMessage');
    // If there's a pending message, start with an empty chat.
    // Otherwise, show the default welcome message.
    return pendingMessage ? [] : [{ type: 'ai', text: "Welcome to the chat! How can I help you today?" }];
  });
  // Uncomment to add User session tracking
  // const { session } = useSession(); 

  const handleSubmit = async (userInput) => {
    const userMessage = { type: 'user', text: userInput };
    setMessages(prev => [...prev, userMessage]);

    /* Session reminder to login
    if (!session) {
      const aiMessage = { type: 'ai', text: "Please log in to chat with Benny." };
      setMessages(prev => [...prev, aiMessage]);
      return;
    }
    */

    try {
      const res = await axios.post(
        `${API_URL}/chat`,
        { message: userInput },
        /*  Add the user session token with message 

        Currently the backend does not accept session.token headers and will
        default to the "Sorry, something went wrong", if this is uncommented

        { headers: { Authorization: `Bearer ${session.token}` } } 
         
        */
      );

      let aiMessage;
      if (res.data && res.data.success) {
        aiMessage = { type: 'ai', text: res.data.response };
      } else {
        // If API stops working
        aiMessage = { type: 'ai', text: res.data.response || "Sorry, something went wrong." };
      }
      setMessages(prev => [...prev, aiMessage]);

    } catch (error) {
      console.error("Failed to send message:", error);
      let errorMessage = "Sorry, I couldn't connect to the server.";
      if (error.response && error.response.data && error.response.data.response) {
        errorMessage = error.response.data.response;
      }
      const aiMessage = { type: 'ai', text: errorMessage };
      setMessages(prev => [...prev, aiMessage]);
    }
  };
  
  // On component mount, check for a pending message from the homepage
  useEffect(() => {
    const pendingMessage = sessionStorage.getItem('pendingMessage');
    if (pendingMessage) {
      // If a message is found, submit it to the chat
      handleSubmit(pendingMessage);
      // Clean up sessionStorage to prevent the message from being sent again
      sessionStorage.removeItem('pendingMessage');
    }
  }, []); // The empty dependency array ensures this effect runs only once

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <main className="flex flex-col items-center pt-16 px-4">
        <div className="w-full max-w-2xl">
          {messages.map((msg, idx) =>
            msg.type === 'ai' ? (
              <ChatBubble key={idx} message={msg.text} icon={bennyIcon} />
            ) : (
              <div key={idx} className="flex justify-end mb-4">
                <div className="bg-blue-100 p-4 rounded-lg">
                  <p>{msg.text}</p>
                </div>
              </div>
            )
          )}
          <ChatInput onSubmit={handleSubmit} />
        </div>
      </main>
    </div>
  );
}

export default Chat;