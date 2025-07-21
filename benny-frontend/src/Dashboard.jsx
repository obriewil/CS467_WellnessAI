import React, { useState } from 'react';
import axios from 'axios';
import Header from './components/Header';
import { FaUserCircle, FaEnvelope, FaLock } from 'react-icons/fa';

const PasswordChangeModal = ({ isOpen, onClose, onSubmit }) => {
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ oldPassword, newPassword });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
      <div className="relative bg-white rounded-lg shadow-2xl p-8 w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6">Change Password</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Current Password</label>
            <input
              type="password"
              value={oldPassword}
              onChange={(e) => setOldPassword(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">New Password</label>
            <input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              required
            />
          </div>
          <div className="pt-4 flex justify-end gap-3">
            <button type="button" onClick={onClose} className="bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded-lg hover:bg-gray-300">
              Cancel
            </button>
            <button type="submit" className="bg-black text-white font-semibold py-2 px-4 rounded-lg hover:bg-gray-800">
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};


const Dashboard = () => {
  const mockUser = {
    name: 'Alex Doe',
    email: 'alex.doe@example.com',
  };

  // 2. Add state to control the password modal visibility
  const [isPasswordModalOpen, setIsPasswordModalOpen] = useState(false);

  // 3. Placeholder function for changing the password
  const handleChangePassword = async ({ oldPassword, newPassword }) => {
    console.log("Attempting to change password...");
    try {
      // This is where the actual API call will go.
      // It's commented out because we are not connected to a backend yet.
      /*
      const response = await axios.post('/api/users/change-password', {
        oldPassword,
        newPassword,
      });
      */
      
      // Simulate a successful API call for the demo
      alert("Password changed successfully! (Demo)");
      setIsPasswordModalOpen(false); // Close the modal on success

    } catch (error) {
      console.error("Failed to change password:", error);
      alert("Failed to change password. See console for details. (Demo)");
    }
  };

  // 4. Placeholder function for logging out
  const handleLogout = async () => {
    console.log("Attempting to log out...");
    try {
      // The actual API call to invalidate the session/token on the backend
      /*
      await axios.post('/api/v1/auth/logout');
      */
      
      // For the demo, we'll just redirect to the home page
      alert("Logging you out... (Demo)");
      window.location.href = '/';

    } catch (error) {
      console.error("Failed to log out:", error);
      alert("Logout failed. See console for details. (This is a demo)");
    }
  };


  return (
    <>
      <Header />
      <div className="bg-gray-50 min-h-screen py-10 px-4">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-4xl font-bold text-gray-800 mb-8">User Settings</h1>
          <div className="bg-white p-8 rounded-lg shadow-md mb-8">
            <h2 className="text-2xl font-semibold text-gray-700 mb-6 border-b pb-4">Profile Information</h2>
            <div className="space-y-6">
              <div className="flex items-center">
                <FaUserCircle className="text-gray-400 mr-4" size={24} />
                <div>
                  <label className="block text-sm font-medium text-gray-500">Full Name</label>
                  <p className="text-lg text-gray-900">{mockUser.name}</p>
                </div>
              </div>
              <div className="flex items-center">
                <FaEnvelope className="text-gray-400 mr-4" size={24} />
                <div>
                  <label className="block text-sm font-medium text-gray-500">Email Address</label>
                  <p className="text-lg text-gray-900">{mockUser.email}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Account Security Section */}
          <div className="bg-white p-8 rounded-lg shadow-md">
            <h2 className="text-2xl font-semibold text-gray-700 mb-6 border-b pb-4">Account Security</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-800">Change Password</p>
                  <p className="text-sm text-gray-500">Set a permanent password for your account.</p>
                </div>
                <button 
                  onClick={() => setIsPasswordModalOpen(true)}
                  className="bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded-lg hover:bg-gray-300"
                >
                  Set Password
                </button>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-800">Log Out</p>
                  <p className="text-sm text-gray-500">You will be returned to the home page.</p>
                </div>
                <button 
                  onClick={handleLogout}
                  className="bg-red-100 text-red-700 font-semibold py-2 px-4 rounded-lg hover:bg-red-200"
                >
                  Log Out
                </button>
              </div>
            </div>
          </div>

        </div>
      </div>

      <PasswordChangeModal 
        isOpen={isPasswordModalOpen} 
        onClose={() => setIsPasswordModalOpen(false)}
        onSubmit={handleChangePassword}
      />
    </>
  );
};

export default Dashboard;