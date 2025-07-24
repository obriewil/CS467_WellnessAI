// src/components/Header.jsx

import React, { useState } from 'react';
import { useSession } from '../contexts/SessionContext';
import siteIcon from '../assets/site_icon.png';
import { Link } from 'react-router-dom';
import AuthModal from './Auth'; 

const Header = () => { 
  const { session, loading, logout } = useSession();
  
  const [showSignUp, setShowSignUp] = useState(false);

  return (
    <>
      <header className="w-full p-4 flex items-center justify-between border-b border-gray-200 bg-white">
        <Link to="/" className="flex items-center">
          <div className="p-1 rounded-md">
            <img src={siteIcon} alt="Site Icon" className="w-12 h-12 ml-10" />
          </div>
          <h1 className="text-xl font-semibold text-gray-800 ml-0">Benny</h1>
        </Link>

        <div className="mr-10">
          {loading ? (
            <div className="w-24 h-8 bg-gray-200 rounded animate-pulse"></div>
          ) : session ? (
            <div className="flex items-center gap-4">
              <Link to="/dashboard" className="font-semibold text-gray-700 hover:text-black">
                Welcome, {session.user.name}!
              </Link>
              <button onClick={logout} className="text-red-600 font-semibold hover:text-red-800 transition-colors">
                Log Out
              </button>
            </div>
          ) : (
            <button 
              onClick={() => setShowSignUp(true)} 
              className="text-blue-600 font-semibold hover:text-blue-800 transition-colors"
            >
              Sign Up
            </button>
          )}
        </div>
      </header>
      
      <AuthModal
        isOpen={showSignUp}
        onClose={() => setShowSignUp(false)}
      />
    </>
  );
};

export default Header;