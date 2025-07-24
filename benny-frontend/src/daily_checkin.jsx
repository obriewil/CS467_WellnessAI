import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import { checkinFlow } from './checkinFlow';
import ChatBubble from './components/ChatBubble';
import bennyIcon from './assets/benny_icon.png'; 

const DailyCheckin = () => {
  const [messages, setMessages] = useState([]);
  const [currentStep, setCurrentStep] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);

  useEffect(() => {
    setMessages([checkinFlow[0]]);
  }, []);

  const handleButtonClick = (buttonText) => {
    if (isCompleted) return;

    // 1. Create the user's message object from the button they clicked.
    const userMessage = { type: 'user', text: buttonText };

    // 2. Add the user's message to the chat history to display it.
    setMessages(prevMessages => [...prevMessages, userMessage]);

    // 3. Move to the next step in the conversation flow.
    const nextStep = currentStep + 1;
    if (nextStep < checkinFlow.length) {
      const nextAiMessage = checkinFlow[nextStep];

      // 4. Simulate the AI "typing".
      setTimeout(() => {
        setMessages(prevMessages => [...prevMessages, nextAiMessage]);
        setCurrentStep(nextStep);
        if (!nextAiMessage.buttons || nextAiMessage.buttons.length === 0) {
          setIsCompleted(true);
        }
      }, 1000); 
    }
  };

  return (
    <>
      <Header />
      <main className="flex flex-col items-center pt-16 px-4 bg-white min-h-screen">
        <img src={bennyIcon} alt="Benny the Beaver" className="w-20 h-20 mb-4" />
        <h2 className="text-3xl font-bold mb-2 text-gray-800">Recipe Planner</h2>
        <p className="text-gray-500 mb-8">pee pee poo poo</p>

        {/* This div contains the chat bubbles */}
        <div className="w-full max-w-3xl">
          {messages.map((msg, idx) => {
            if (msg.type === 'ai') {
              return (
                <ChatBubble
                  key={idx}
                  message={msg.text}
                  icon={msg.icon}
                  buttons={msg.buttons}
                  onButtonClick={handleButtonClick}
                />
              );
            }
            // Render the user's response from clicking a button
            return (
              <div key={idx} className="flex justify-end mb-4">
                <div className="bg-black text-white font-semibold p-3 rounded-lg max-w-md">
                  <p>{msg.text}</p>
                </div>
              </div>
            );
          })}
        </div>
      </main>
    </>
  );
};

export default DailyCheckin;