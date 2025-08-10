import React, { useState } from 'react';
import { FaPaperPlane } from 'react-icons/fa';

const ChatInput = ({ onSubmit }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSubmit(input);
      setInput('');
    }
  };

  const buttonStyle = {
    color: input.trim() ? '#D73F09' : '#F9A887', 
    transition: 'color 150ms ease-in-out', 
  };

  const textareaStyle = {
    backgroundColor: '#ffffff',
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="relative">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Share your thoughts here... What would you like to improve?"
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSubmit(e);
            }
          }}
          className="w-full border border-gray-300 p-4 pr-16 rounded-xl text-2xl resize-none placeholder-gray-350 focus:outline-none focus:border-osu-orange focus:ring-1 focus:ring-osu-orange"
          rows={4}
          style={textareaStyle}
        />
        <button
          type="submit"
          className="absolute bottom-4 right-4 disabled:opacity-50"
          style={buttonStyle}
          disabled={!input.trim()}
        >
          <FaPaperPlane size={24} />
        </button>
      </div>
    </form>
  );
};

export default ChatInput;