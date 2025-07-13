import React, { useEffect } from 'react';
import { FaGoogle, FaApple, FaFacebook } from "react-icons/fa";
import siteIcon from '../assets/site_icon.png';
import { useSession } from '../contexts/SessionContext';

// base URL for FastAPI backend
const API_BASE_URL = 'http://localhost:8000';

const AuthModal = ({ isOpen, onClose }) => {
  const { login } = useSession();

  // pop-up login
  useEffect(() => {
    const handleAuthMessage = (event) => {
      // extract login token
      const { token } = event.data;
      if (token) {
        login(token);
        onClose();
      }
    };

    window.addEventListener('message', handleAuthMessage);

    return () => {
      window.removeEventListener('message', handleAuthMessage);
    };
  }, [login, onClose]);

  const openAuthPopup = (provider) => {
    const width = 600;
    const height = 700;
    const left = (window.innerWidth / 2) - (width / 2);
    const top = (window.innerHeight / 2) - (height / 2);
    
    // Login endpoint on our FastAPI backend
    const url = `${API_BASE_URL}/api/v1/auth/${provider}/login`;

    window.open(url, 'authPopup', `width=${width},height=${height},top=${top},left=${left}`);
  };

  if (!isOpen) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm" onClick={onClose}>
      <div className="relative bg-white rounded-2xl shadow-2xl p-8 w-full max-w-lg flex flex-col items-center" onClick={e => e.stopPropagation()}>
        <img src={siteIcon} alt="Logo" className="w-16 h-16 mb-4 rounded-full" />
        <h2 className="text-3xl font-bold mb-2 text-gray-900">Login Page</h2>
        <p className="text-gray-600 mb-8 text-center text-base">Gnaw away at your health goals</p>
        
        <div className="w-full space-y-4 mb-6">
          <button 
            onClick={() => openAuthPopup('google')} 
            className="w-full bg-blue-500 text-white font-semibold py-3 rounded-lg flex items-center justify-center gap-3 hover:bg-blue-600 transition-colors text-lg"
          >
            <FaGoogle size={20} /> Continue with Google
          </button>
          
          <button 
            onClick={() => openAuthPopup('apple')} 
            className="w-full bg-black text-white font-semibold py-3 rounded-lg flex items-center justify-center gap-3 hover:bg-gray-800 transition-colors text-lg"
          >
            <FaApple size={22} /> Continue with Apple
          </button>
          
          <button 
            onClick={() => openAuthPopup('facebook')} 
            className="w-full bg-indigo-700 text-white font-semibold py-3 rounded-lg flex items-center justify-center gap-3 hover:bg-indigo-800 transition-colors text-lg"
          >
            <FaFacebook size={22} /> Continue with Facebook
          </button>
        </div>

        <p className="text-sm text-gray-600 my-4">
          Terms and Service, links should go here?
        </p>

        {/* close popup*/}
        <button onClick={onClose} className="absolute top-4 right-4 text-gray-500 hover:text-gray-700">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default AuthModal;