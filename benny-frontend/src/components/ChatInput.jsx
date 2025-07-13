import React, { useState } from 'react';

const ChatInput = ({ onSubmit }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSubmit(input);
      setInput('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col">
        <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Share your thoughts here... What would you like to improve about your health and wellness?"
        className="w-full border border-gray-300 p-5 rounded mb-2 h-24 resize-none"
        />
      <button type="submit" className="bg-black text-white p-2 rounded">
        Continue
      </button>
    </form>
  );
};


export default ChatInput;