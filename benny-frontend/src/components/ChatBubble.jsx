import React, { useState, useEffect, useRef } from 'react';

const ChatBubble = ({ message, icon }) => {
  const [displayedText, setDisplayedText] = useState('');
  const indexRef = useRef(0);

  useEffect(() => {
    indexRef.current = 0;
    setDisplayedText('');
    const timer = setInterval(() => {
      if (indexRef.current < message.length) {
        indexRef.current += 1;
        setDisplayedText(message.slice(0, indexRef.current));
      } else {
        clearInterval(timer);
      }
    }, 15); // This handles the speed of the chat bubble.
    return () => clearInterval(timer);
  }, [message]);

  return (
    <div className="flex items-start mb-4">
      <img src={icon} alt="Benny" className="w-8 h-8 mr-2 rounded-full" />
      <div className="bg-gray-100 p-4 rounded-lg">
        <p>{displayedText}</p>
      </div>
    </div>
  );
};

export default ChatBubble;