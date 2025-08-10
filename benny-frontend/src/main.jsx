import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';

// Context and Components
import { SessionProvider } from './contexts/SessionContext';
import App from './App.jsx';
import DailyCheckin from './daily_checkin.jsx';
import WellnessPriorities from './WellnessPriorities.jsx';
import Dashboard from './Dashboard.jsx';
import Chat from './chat.jsx';
import ChatHistory from './chatHistory';
import ProtectedLayout from './components/ProtectedLayout'; // <-- Import the new layout

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <SessionProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<App />} />

          <Route element={<ProtectedLayout />}>
            <Route path="/chat" element={<Chat />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/chat-history" element={<ChatHistory />} />
            <Route path="/daily-checkin" element={<DailyCheckin />} />
            <Route path="/priorities" element={<WellnessPriorities />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </SessionProvider>
  </StrictMode>
);