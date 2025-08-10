import React, { useState } from 'react';
import { useSession } from '../contexts/SessionContext';
import { Link } from 'react-router-dom';
import AuthModal from './Auth';

const Header = ({ isDashboardPage = false }) => {
  const { session, loading, logout } = useSession();
  const [showSignUp, setShowSignUp] = useState(false);
  
  return (
    <>
      <header 
        className="w-full p-4 flex items-center justify-end"
        style={{ backgroundColor: '#f7f5f5' }}
      >
        <div className="mr-4">
          {loading ? (
            <div className="w-24 h-8 bg-gray-200 rounded animate-pulse"></div>
          ) : session ? (
            <div className="flex items-center gap-4">
              <span className="font-semibold text-gray-700">
                {session.user.name}!
              </span>
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