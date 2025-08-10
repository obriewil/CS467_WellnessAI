import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ChatBubble from './components/ChatBubble';
import ChatInput from './components/ChatInput';
import bennyIcon from './assets/benny_icon.png';
import { useTypingEffect } from './hooks/useTypingEffect';

const API_URL = import.meta.env.VITE_API_URL;

const GREETING_PROMPTS = [
  "Hi, I can help with nutrition, fitness, and stress. Where would you like to start?",
  "Hey! I'm all about helping you eat better, move more, and stress less. What's on your mind?",
  "Are you looking to boost your energy with better food, get stronger with fitness, or find your calm?",
];

function Chat() {
  const [messages, setMessages] = useState(() => {
    const pendingMessage = sessionStorage.getItem('pendingMessage');
    if (pendingMessage) return [];
    const randomIndex = Math.floor(Math.random() * GREETING_PROMPTS.length);
    return [{ type: 'ai', text: GREETING_PROMPTS[randomIndex] }];
  });
  
  const chatEndRef = useRef(null);
  const initialMessageText = messages.length > 0 && messages[0].type === 'ai' ? messages[0].text : "";
  const animatedGreeting = useTypingEffect(initialMessageText, 20);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (userInput) => {
    const userMessage = { type: 'user', text: userInput };

    // This is the only change. It checks if this is the first message.
    const isFirstMessage = messages.length <= 1 && (!messages[0] || messages[0].type === 'ai');

    if (isFirstMessage) {
      // If it is, we replace the welcome message with the user's first message.
      setMessages([userMessage]);
    } else {
      // Otherwise, we just add the new message to the list.
      setMessages(prev => [...prev, userMessage]);
    }

    try {
      const res = await axios.post(`${API_URL}/chat`, { message: userInput });
      let aiMessage = { type: 'ai', text: res.data.response || "Sorry, something went wrong." };
      // This will correctly append the AI response to the new message history
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
  
  useEffect(() => {
    const pendingMessage = sessionStorage.getItem('pendingMessage');
    if (pendingMessage) {
      handleSubmit(pendingMessage);
      sessionStorage.removeItem('pendingMessage');
    }
  }, []);

  const showWelcomeScreen = messages.length <= 1 && (!messages[0] || messages[0].type === 'ai');

  return (
    <div className="flex flex-col h-full">
      {showWelcomeScreen ? (
        <div className="flex flex-col items-center justify-center text-center flex-grow pb-88">
          <div className="w-full max-w-3xl">
            <img src={bennyIcon} alt="Benny the Beaver" className="w-50 h-50 mb-0 mx-auto" />
            <h2 className="text-4xl font-bold -mt-3 mb-4 text-gray-800">Benny WellnessAI</h2>
            <p className="text-gray-500 max-w-none mx-auto mb-8">
              {animatedGreeting}
            </p>
            <ChatInput onSubmit={handleSubmit} />
          </div>
        </div>
      ) : (
        <>
          <div className="flex-grow w-full max-w-3xl mx-auto overflow-y-auto p-4">
            {messages.map((msg, idx) =>
              msg.type === 'ai' ? (
                <ChatBubble key={idx} message={msg.text} icon={bennyIcon} />
              ) : (
                <div key={idx} className="flex justify-end mb-4">
                  <div className="bg-blue-100 p-4 rounded-lg">
                    <p className="text-xl">{msg.text}</p>
                  </div>
                </div>
              )
            )}
            <div ref={chatEndRef} />
          </div>
          <div className="w-full max-w-3xl mx-auto pt-4">
            <ChatInput onSubmit={handleSubmit} />
          </div>
        </>
      )}
    </div>
  );
}

export default Chat;