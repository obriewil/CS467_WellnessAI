import React, { useState, useEffect } from 'react';
import { useSession } from './contexts/SessionContext';
import { useNavigate } from 'react-router-dom';
import ChatBubble from './components/ChatBubble';
import ChatInput from './components/ChatInput';
import AuthModal from './components/Auth';
import Header from './components/Header';
import bennyIcon from './assets/benny_icon.png';

const GREETING_PROMPTS = [
  "Hi, I'm Benny, your wellness beaver! I can help with nutrition, fitness, and stress. Where would you like to start?",
  "Hey! Benny the wellness beaver, at your service. I'm all about helping you eat better, move more, and stress less. What's top of mind for you?",
  "Hi, I'm Benny! My goal is to help you feel great. Are you looking to boost your energy with better food, get stronger with fitness, or find your calm? Let me know!",
];

function App() {
  const [messages, setMessages] = useState(() => {
    const randomIndex = Math.floor(Math.random() * GREETING_PROMPTS.length);
    return [{ type: 'ai', text: GREETING_PROMPTS[randomIndex] }];
  });
  const [showSignUp, setShowSignUp] = useState(false);
  const { session, loading, login } = useSession();
  const navigate = useNavigate();

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    if (token) {
      login(token);
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, [login]);

  useEffect(() => {
    if (!loading && session) {
      navigate('/chat');
    }
  }, [session, loading, navigate]);

  const handleSubmit = async (userInput) => {
    const userMessage = { type: 'user', text: userInput };
    setMessages(prev => [...prev, userMessage]);
    sessionStorage.setItem('pendingMessage', userInput);
    const aiMessage = { type: 'ai', text: "Thanks! Let's get you signed in to continue." };
    setTimeout(() => {
      setMessages(prev => [...prev, aiMessage]);
      const typingDelay = aiMessage.text.length * 30 + 300;
      setTimeout(() => {
        setShowSignUp(true);
      }, typingDelay);
    }, 500);
  };

  if (loading || session) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: '#f7f5f5' }}>
        <div className="font-semibold text-gray-600">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#f7f5f5' }}>
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
      <AuthModal isOpen={showSignUp} onClose={() => setShowSignUp(false)} />
    </div>
  );
}

export default App;