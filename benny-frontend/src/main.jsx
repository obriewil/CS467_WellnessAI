import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import App from './App.jsx';
import DailyCheckin from './daily_checkin.jsx';
import WellnessPriorities from './WellnessPriorities.jsx';
import Dashboard from './Dashboard.jsx';
import { SessionProvider } from './contexts/SessionContext';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <SessionProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/daily-checkin" element={<DailyCheckin />} />
          <Route path="/priorities" element={<WellnessPriorities />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </BrowserRouter>
    </SessionProvider>
  </StrictMode>
);