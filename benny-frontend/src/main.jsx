// src/main.jsx

import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import App from './App.jsx';
import DailyCheckin from './daily_checkin.jsx';
import WellnessPriorities from './WellnessPriorities.jsx';
import Dashboard from './Dashboard.jsx';
import Chat from './Chat.jsx';
import { SessionProvider } from './contexts/SessionContext';
import ChatHistory from './chatHistory';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <SessionProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/daily-checkin" element={<DailyCheckin />} />
          <Route path="/priorities" element={<WellnessPriorities />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/chat" element={<Chat />} /> 
          <Route path="/chat-history" element={<ChatHistory />} />
        </Routes>
      </BrowserRouter>
    </SessionProvider>
  </StrictMode>
);