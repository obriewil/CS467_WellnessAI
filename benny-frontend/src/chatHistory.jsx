import React, { useEffect, useState } from 'react';
import axios from 'axios';
import bennyIcon from './assets/benny_icon.png';
import { FaHistory } from 'react-icons/fa';

const BACKEND_URL = 'http://127.0.0.1:8000';

const ChatHistory = () => {
    const [recentMessages, setRecentMessages] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadRecentMessages();
    }, []);

    const loadRecentMessages = async () => {
        try {
            setLoading(true);
            const response = await axios.get(`${BACKEND_URL}/api/chat/recent`);
            if (response.data.success) {
                setRecentMessages(response.data.messages);
            }
        } catch (error) {
            console.error('Error loading recent messages:', error);
            setError('Failed to load chat history');
        } finally {
            setLoading(false);
        }
    };

    const formatDateTime = (dateString) => {
        if (!dateString) return '';
        const [month, day, year] = dateString.split('/');
        // Handle potential invalid date strings gracefully
        if (!month || !day || !year) return dateString;
        
        const date = new Date(year, month - 1, day);
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
        });
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white-900"></div>
                <span className="ml-3">Loading recent chats...</span>
            </div>
        );
    }

    return (
        <div className="w-full max-w-2xl mx-auto text-center">
            <img src={bennyIcon} alt="Benny the Beaver" className="w-20 h-20 mb-4 mx-auto" />
            <h2 className="text-3xl font-bold mb-2 text-white-800">Chat History</h2>
            <p className="text-gray-500 mb-8">Your recent conversations with Benny</p>

            {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6 w-full">
                {error}
            </div>
            )}

            <div className="text-left">
                {recentMessages.length === 0 ? (
                    <div className="text-center py-12">
                        <FaHistory className="text-6xl text-gray-300 mx-auto mb-4" />
                        <h3 className="text-xl font-medium text-gray-600 mb-2">
                            No chat history yet
                        </h3>
                        <p className="text-gray-500">
                            Start chatting with Benny to see your conversation history here
                        </p>
                    </div>
                ) : (
                    <>
                        {recentMessages.map((message) => {
                            if (message.user_or_benny === 1) {
                            // Benny's message
                            return (
                                <div key={`${message.date}-${message.sequence_number}`} className="mb-4">
                                <div className="flex items-start">
                                    <img src={bennyIcon} alt="Benny" className="w-8 h-8 mr-2 rounded-full" />
                                    <div className="bg-gray-100 p-4 rounded-lg">
                                    <p>{message.entry_text}</p>
                                    </div>
                                </div>
                                <div className="text-xs text-gray-400 ml-10 mt-1">
                                    {formatDateTime(message.date)}
                                </div>
                        </div>
                    );
                    } else {
                        // User's message
                        return (
                        <div key={`${message.date}-${message.sequence_number}`} className="mb-4">
                            <div className="flex justify-end">
                            <div className="bg-blue-100 p-4 rounded-lg max-w-md">
                                <p>{message.entry_text}</p>
                            </div>
                            </div>
                            <div className="text-xs text-gray-400 text-right mr-2 mt-1">
                            {formatDateTime(message.date)}
                            </div>
                        </div>
                        );
                    }
                })}

                {recentMessages.length > 0 && (
                    <div className="text-center py-6">
                        <p className="text-gray-500 text-sm">
                            Showing your {recentMessages.length} most recent messages
                        </p>
                    </div>
                )}
                </>
            )}
            </div>
        </div>
    );
};

export default ChatHistory;