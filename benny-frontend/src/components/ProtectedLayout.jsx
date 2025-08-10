import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';

const ProtectedLayout = () => {
  const [isSidebarExpanded, setSidebarExpanded] = useState(false);

  const toggleSidebar = () => {
    setSidebarExpanded(!isSidebarExpanded);
  };

  return (
    <div 
      className="relative min-h-screen" 
      style={{ backgroundColor: '#f7f5f5' }}
    >
      <Sidebar isExpanded={isSidebarExpanded} onToggle={toggleSidebar} />
      
      <div 
        className={`transition-all duration-300 ease-in-out flex flex-col h-screen ${
          isSidebarExpanded ? 'ml-64' : 'ml-20'
        }`}
      >
        <Header />
        
        <main className="flex-grow p-6 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default ProtectedLayout;