import React, { useState, useEffect } from 'react';
import axios from 'axios'; // This is unused rn but once we have auth it sends the first user msg to the LLM
import { useSession } from './contexts/SessionContext';
import { useNavigate } from 'react-router-dom';
import ChatBubble from './components/ChatBubble';
import ChatInput from './components/ChatInput';
import AuthModal from './components/Auth';
import Header from './components/Header'; // Import the shared Header
import siteIcon from './assets/site_icon.png';
import bennyIcon from './assets/benny_icon.png';

const GREETING_PROMPTS = [
  "Hi, I'm Benny, your wellness beaver! I can help with nutrition, fitness, and stress. Where would you like to start?",
  "Hey! Benny the wellness beaver, at your service. I'm all about helping you eat better, move more, and stress less. What's top of mind for you?",
  "Hi, I'm Benny! My goal is to help you feel great. Are you looking to boost your energy with better food, get stronger with fitness, or find your calm? Let me know!",
  "Howdy! I'm Benny, and I'm eager to help you build a healthier life. What are we working on first—mighty meals, fun fitness, or steady serenity?",
  "Hello, I'm Benny. I'm here to support your journey to better well-being. To get started, what's one thing you'd like to improve or feel better about?"
];

function App() {
  const [messages, setMessages] = useState(() => {
    const randomIndex = Math.floor(Math.random() * GREETING_PROMPTS.length);
    const randomPromptText = GREETING_PROMPTS[randomIndex];
    return [{ type: 'ai', text: randomPromptText }];
  });

  const [showSignUp, setShowSignUp] = useState(false);

  const { session, loading, login } = useSession();
  const navigate = useNavigate();

  // This effect runs on component mount to check for a token in the URL
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');

    if (token) {
      login(token);
      
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, [login]);

  // If the user is logged in, redirect them from the landing page to the chat.
  useEffect(() => {
    if (!loading && session) {
      navigate('/chat');
    }
  }, [session, loading, navigate]);

// Submission of a new message from the user
const handleSubmit = async (userInput) => {
  const userMessage = { type: 'user', text: userInput };
  setMessages(prev => [...prev, userMessage]);

  let aiMessage;
  if (session) {
    try {
      // This would normally go to an LLM
      aiMessage = { type: 'ai', text: "Redirecting you to the chat!" };
      navigate('/chat'); // Navigate on first message if somehow they are on this page
    } catch (error) {
      console.error("Failed to send message:", error);
      aiMessage = { type: 'ai', text: "Error" };
    }
  } else {
    // If user is not logged in, save the message and show the login modal
    sessionStorage.setItem('pendingMessage', userInput);
    aiMessage = { type: 'ai', text: "Thanks! Let's get you signed in to continue." };
  }

  // Simulate delay for AI response
  setTimeout(() => {
    setMessages(prev => [...prev, aiMessage]);
    if (!session) {
      const typingDelay = aiMessage.text.length * 30 + 300;
      setTimeout(() => {
        setShowSignUp(true);
      }, typingDelay);
    }
  }, 500);
};

  // Render a loading state while checking for session to prevent flashing the wrong UI
  if (loading || session) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="font-semibold text-gray-600">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white">
      <Header />
      
      <main className="flex flex-col items-center pt-16 px-4">
        <img src={bennyIcon} alt="Benny the Beaver" className="w-20 h-20 mb-4" />
        <h2 className="text-3xl font-bold mb-2 text-gray-800">Set Your Focus</h2>
        <p className="text-gray-500 mb-8">Let's start your wellness journey together</p>
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

      <AuthModal
        isOpen={showSignUp}
        onClose={() => setShowSignUp(false)}
      />
    </div>
  );
}

export default App;