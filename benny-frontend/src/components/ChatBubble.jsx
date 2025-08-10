import React from 'react';
import { useTypingEffect } from '../hooks/useTypingEffect';

const ChatBubble = ({ message, icon, buttons, onButtonClick }) => {
  const displayedText = useTypingEffect(message);
  const isTypingComplete = displayedText === message;

  return (
    <div className="flex items-start mb-4">
      <img src={icon} alt="Benny" className="w-12 h-12 -mr-2 mt-2 rounded-full" />
      <div className="bg-gray-0 p-4 rounded-lg">
        <p className="text-xl">{displayedText}</p>
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