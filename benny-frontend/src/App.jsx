import React, { useState, useEffect } from 'react';
import axios from 'axios'; // This is unused rn but once we have auth it sends the first user msg to the LLM
import { useSession } from './contexts/SessionContext';
import ChatBubble from './components/ChatBubble';
import ChatInput from './components/ChatInput';
import AuthModal from './components/Auth';
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

  const { session, loading, login, logout } = useSession();

  // This effect runs on component mount to check for a token in the URL
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');

    if (token) {
      login(token);
      
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, [login]);

// Submission of a new message from the user
const handleSubmit = async (userInput) => {
  const userMessage = { type: 'user', text: userInput };
  setMessages(prev => [...prev, userMessage]);

  let aiMessage;
  if (session) {
    try {
      // Probably send this to the LLM after the user is signed? Probably store the message then send it later? 
      // const res = await axios.post(
      //   'http://localhost:8000/api/v1/chat', 
      //   { message: userInput },
      //   { headers: { Authorization: `Bearer ${session.token}` } }
      // );
      // aiMessage = { type: 'ai', text: res.data.response };
    } catch (error) {
      console.error("Failed to send message:", error);
      aiMessage = { type: 'ai', text: "Error" };
    }
  } else {
    // For now it's a boiler plate response, until sign up
    aiMessage = { type: 'ai', text: "Thanks! Let's proceed." };
  }

  // Simulate delay for AI response
  setTimeout(() => {
    setMessages(prev => [...prev, aiMessage]);
    if (!session) {
      // delay for typing animation before login popup
      const typingDelay = aiMessage.text.length * 30 + 300;
      setTimeout(() => {
        setShowSignUp(true);
      }, typingDelay);
    }
  }, 500); // 500 handles the speed of the message
  // if looking for speed of OG prompt check ChatBubble.jsx
};

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="min-h-screen bg-white">
      <header className="w-full p-4 flex items-center justify-between border-b border-gray-200">
        <div className="flex items-center">
          <div className="p-1 rounded-md">
            <img src={siteIcon} alt="Site Icon" className="w-12 h-12 ml-10" />
          </div>
          <h1 className="text-xl font-semibold text-gray-800 ml-0">Benny</h1>
        </div>

        {/* Conditionally render the header based on authentication state */}
        <div className="mr-10">
          {loading ? (
            // Verification spinner I copied off a tutorial
            <div className="w-24 h-8 bg-gray-200 rounded animate-pulse"></div>
          ) : session ? (
            <div className="flex items-center gap-4">
              <span>Welcome, {session.user.name}!</span>
              <button onClick={handleLogout} className="text-red-600 font-semibold hover:text-red-800 transition-colors">
                Log Out
              </button>
            </div>
          ) : (
            // If the user is not logged in, show the sign-up button
            <button 
              onClick={() => setShowSignUp(true)} 
              className="text-blue-600 font-semibold hover:text-blue-800 transition-colors"
            >
              Sign Up
            </button>
          )}
        </div>
      </header>
      
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