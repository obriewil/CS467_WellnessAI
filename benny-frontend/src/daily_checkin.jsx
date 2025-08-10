import React, { useState, useEffect } from 'react';
import { checkinQuestions } from './checkinQuestions';
import axios from 'axios';
import ChatBubble from './components/ChatBubble';
import bennyIcon from './assets/benny_icon.png';

const BACKEND_URL = 'http://127.0.0.1:8000';

const DailyCheckin = () => {
    const [messages, setMessages] = useState([]);
    const [currentStep, setCurrentStep] = useState(0);
    const [isCompleted, setIsCompleted] = useState(false);
    const [responses, setResponses] = useState([]);
    const [backendConnected, setBackendConnected] = useState(false);
    const [bennyRecommendation, setBennyRecommendation] = useState(null);

    useEffect(() => {
        testBackendConnection();
        initializeCheckin();
    }, []);

    useEffect(() => {
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
            setBackendConnected(true);
            console.log('Backend status:', response.data);
        } catch (err) {
            console.warn('Backend unavailable', err);
            setBackendConnected(false);
        }
    };

    const initializeCheckin = () => {
        setMessages([checkinQuestions[0]]);
    };

    const handleButtonClick = async (buttonText) => {
        if (isCompleted) return;

        const currentQuestion = checkinQuestions[currentStep];
        const newResponse = {
            category: currentQuestion.category,
            question: currentQuestion.text,
            response: buttonText
        };

        const updatedResponses = [...responses, newResponse];
        setResponses(updatedResponses);

        const userMessage = { type: 'user', text: buttonText };
        setMessages(prevMessages => [...prevMessages, userMessage]);

        const nextStep = currentStep + 1;
        if (nextStep < checkinQuestions.length) {
            const nextAiMessage = checkinQuestions[nextStep];

            if (nextAiMessage.category === 'completion') {
                await submitCheckin(updatedResponses);
            }

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
            const response = await axios.post(`${BACKEND_URL}/api/checkin/submit`, {
                responses: finalResponses
            });

            if (response.data.success) {
                console.log('Check in submitted successfully');
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
        <div className="w-full max-w-3xl mx-auto text-center">
            <img src={bennyIcon} alt="Benny the Beaver" className="w-20 h-20 mb-4 mx-auto" />
            <h2 className="text-3xl font-bold mb-2 text-gray-800">Daily Checkin</h2>
            <p className="text-gray-500 mb-8">Let's see how you're doing today</p>

            <div className="text-left">
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
                    return (
                        <div key={idx} className="flex justify-end mb-4">
                            <div className="bg-black text-white font-semibold p-3 rounded-lg max-w-md">
                                <p>{msg.text}</p>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default DailyCheckin;