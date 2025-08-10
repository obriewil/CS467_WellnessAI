import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; 
import { FaCommentDots, FaCalendar, FaHistory } from 'react-icons/fa';
import siteIcon from '../assets/site_icon.png';

const Sidebar = ({ isExpanded, onToggle }) => {
  const [hoveredLink, setHoveredLink] = useState(null);

  const handleNewChatClick = (e) => {
    e.preventDefault(); 
    window.location.href = '/chat';
  };

  const getLinkStyle = (linkName) => ({
    color: hoveredLink === linkName ? '#D73F09' : '#a0aec0',
    backgroundColor: hoveredLink === linkName ? '#f7f5f5' : 'transparent',
    transition: 'color 150ms ease-in-out, background-color 150ms ease-in-out',
  });

  return (
    <div
      className={`fixed top-0 left-0 h-full bg-white shadow-lg transition-all duration-300 ease-in-out z-50 ${
        isExpanded ? 'w-50' : 'w-20'
      }`}
    >
      <div 
        onClick={onToggle}
        className="flex items-center mb-10 cursor-pointer p-4 rounded-lg hover:bg-osu-light-gray transition-colors"
        aria-label="Toggle sidebar"
      >
        <img src={siteIcon} alt="Site Icon" className="w-12 h-12 flex-shrink-0" />
        {isExpanded && (
          <span className="ml-2 text-xl font-semibold text-osu-gray">
            Benny
          </span>
        )}
      </div>

      <nav className="px-4">
        <ul>
          <li className="mb-4">
            <Link 
              to="/chat" 
              onClick={handleNewChatClick} 
              className="flex items-center p-3 rounded-lg h-10" 
              style={getLinkStyle('chat')} 
              onMouseEnter={() => setHoveredLink('chat')} 
              onMouseLeave={() => setHoveredLink(null)} 
            >
              <FaCommentDots size={24} className="flex-shrink-0" />
              {isExpanded && (
                <span className="ml-4 font-medium text-l">
                  New Chat
                </span>
              )}
            </Link>
          </li>
          <li className="mb-4">
            <Link 
              to="/daily-checkin" 
              className="flex items-center p-3 rounded-lg h-12"
              style={getLinkStyle('daily-checkin')}
              onMouseEnter={() => setHoveredLink('daily-checkin')}
              onMouseLeave={() => setHoveredLink(null)}
            >
              <FaCalendar size={24} className="flex-shrink-0" />
              {isExpanded && (
                <span className="ml-4 font-medium text-l">
                  Daily Check-In
                </span>
              )}
            </Link>
          </li>
          <li className="mb-4">
            <Link 
              to="/chat-history" 
              className="flex items-center p-3 rounded-lg h-12"
              style={getLinkStyle('chat-history')}
              onMouseEnter={() => setHoveredLink('chat-history')}
              onMouseLeave={() => setHoveredLink(null)}
            >
              <FaHistory size={24} className="flex-shrink-0" />
              {isExpanded && (
                <span className="ml-4 font-medium text-l">
                History
                </span>
              )}
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;