import React, { useState, useEffect } from 'react';
import Header from './components/Header';
// import { checkinFlow } from './checkinFlow';
import { checkinQuestions } from './checkinQuestions';
import axios from 'axios';
import ChatBubble from './components/ChatBubble';
import bennyIcon from './assets/benny_icon.png'; 

const BACKEND_URL = 'http://127.0.0.1:8000';

const DailyCheckin = () => {
  const [messages, setMessages] = useState([]);
  const [currentStep, setCurrentStep] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);
  // ADDED
  const [responses, setResponses] = useState([]);
  const [backendConnected, setBackendConnected] = useState(false);
  const [bennyRecommendation, setBennyRecommendation] = useState(null);


  useEffect(() => {
    // test backend
    testBackendConnection();
    initializeCheckin();
  }, []);


  // Wait for Benny's recommendation
  useEffect(() =>{
    if (bennyRecommendation && isCompleted) {
      setTimeout(() => {
        const recommendationMessage = {
          type: 'ai',
          text: `Benny's Recommendation: ${bennyRecommendation}`,
          buttons: [],
          icon: bennyIcon
        };
        setMessages(prevMessages => [...prevMessages, recommendationMessage]);
      }, 2000);
    }
  }, [bennyRecommendation, isCompleted]);

  const testBackendConnection = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/health`);
      setBackendConnected(true)
      console.log('Backend status:', response.data);
    } catch(err) {
      console.warn('Backend unavailable', err);
      setBackendConnected(false);
    }
  };
  
  const initializeCheckin = () => {
    setMessages([checkinQuestions[0]]);
  }

  const handleButtonClick = async (buttonText) => {
    if (isCompleted) return;

    // map responses for backend
    const currentQuestion = checkinQuestions[currentStep];
    const newResponse = {
      category: currentQuestion.category,
      question: currentQuestion.text,
      response: buttonText
    }

    const updatedResponses = [...responses, newResponse];
    setResponses(updatedResponses);

    // 1. Create the user's message object from the button they clicked.
    const userMessage = { type: 'user', text: buttonText };

    // 2. Add the user's message to the chat history to display it.
    setMessages(prevMessages => [...prevMessages, userMessage]);

    // 3. Move to the next step in the conversation flow.
    const nextStep = currentStep + 1;
    if (nextStep < checkinQuestions.length) {
      const nextAiMessage = checkinQuestions[nextStep];

      // if last question, submit
      if (nextAiMessage.category === 'completion') {
        await submitCheckin(updatedResponses);
      }

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

  const submitCheckin = async (finalResponses) => {
    console.log('Submitting check-in: ', finalResponses);
    
    try {
      // Send to backend
      const response = await axios.post(`${BACKEND_URL}/api/checkin/submit`, {
        responses: finalResponses 
      });
      
      console.log('Submit response:', response.data)

      if (response.data.success) {
        console.log('Check in submitted successfully')

        //  Benny's recommendation for display
        if (response.data.recommendation) {
          setBennyRecommendation(response.data.recommendation);
        }
      } else {
        console.error('check in submission failed.');
      }
    } catch (error) {
      console.error('Error submitting check-in', error);
    }
  };


  return (
    <>
      <Header />
      <main className="flex flex-col items-center pt-16 px-4 bg-white min-h-screen">
        <img src={bennyIcon} alt="Benny the Beaver" className="w-20 h-20 mb-4" />
        <h2 className="text-3xl font-bold mb-2 text-gray-800">Daily Checkin</h2>
        <p className="text-gray-500 mb-8">Let's see how you're doing today</p>

        {/* Backend status */}
        <div className="mb-4 text-sm flex items-center">
          <span className={`inline-block w-2 h-2 rounded-full mr-2 ${backendConnected ? 'bg-green-500' : 'bg-orange-500'}`}></span>
          {backendConnected ? 'Backend connected' : 'Backend offline'}
        </div>

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