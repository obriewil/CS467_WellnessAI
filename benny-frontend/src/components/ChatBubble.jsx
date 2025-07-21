import React, { useState, useEffect, useRef } from 'react';

const ChatBubble = ({ message, icon, buttons, onButtonClick }) => {
  const [displayedText, setDisplayedText] = useState('');
  const [isTypingComplete, setIsTypingComplete] = useState(false);
  const indexRef = useRef(0);

  useEffect(() => {
    setIsTypingComplete(false);
    indexRef.current = 0;
    setDisplayedText('');

    const timer = setInterval(() => {
      if (indexRef.current < message.length) {
        indexRef.current += 1;
        setDisplayedText(message.slice(0, indexRef.current));
      } else {
        // When the message is fully displayed, stop the timer and mark as complete
        clearInterval(timer);
        setIsTypingComplete(true);
      }
    }, 15); // Speed of the typing animation

    // Cleanup function
    return () => clearInterval(timer);
  }, [message]);

  return (
    <div className="flex items-start mb-4">
      <img src={icon} alt="Benny" className="w-8 h-8 mr-2 rounded-full" />
      <div className="bg-gray-100 p-4 rounded-lg">
        <p>{displayedText}</p>
        {/* Only render the buttons if typing is complete AND a buttons array exists */}
        {isTypingComplete && buttons && buttons.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2">
            {buttons.map((buttonText, idx) => (
              <button
                key={idx}
                onClick={() => onButtonClick(buttonText)}
                className="bg-white border border-gray-300 text-gray-700 font-semibold px-4 py-2 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {buttonText}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatBubble;