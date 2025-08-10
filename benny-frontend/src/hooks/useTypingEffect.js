import { useState, useEffect, useRef } from 'react';

export const useTypingEffect = (fullText, speed = 15) => {
  const [displayedText, setDisplayedText] = useState('');
  const indexRef = useRef(0);

  useEffect(() => {
    if (!fullText) return;
    indexRef.current = 0;
    setDisplayedText('');

    const timer = setInterval(() => {
      if (indexRef.current < fullText.length) {
        indexRef.current += 1;
        setDisplayedText(fullText.slice(0, indexRef.current));
      } else {
        clearInterval(timer);
      }
    }, speed);

    return () => clearInterval(timer);
  }, [fullText, speed]);

  return displayedText;
};