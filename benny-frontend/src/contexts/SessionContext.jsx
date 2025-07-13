import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';

const SessionContext = createContext();

export const useSession = () => {
 return useContext(SessionContext);
};

export const SessionProvider = ({ children }) => {
 const [session, setSession] = useState(null);
 const [loading, setLoading] = useState(true);

 useEffect(() => {
 const fetchSession = async () => {
 const token = localStorage.getItem('authToken');
 if (token) {
 try {
 const res = await axios.get('http://localhost:8000/api/v1/users/me', {
 headers: { Authorization: `Bearer ${token}` }
 });
 setSession({ user: res.data, token });
 } catch (error) {
 console.error("Failed to fetch user:", error);
 localStorage.removeItem('authToken');
 }
 }
 setLoading(false);
 };
 fetchSession();
 }, []);

 const login = (token) => {
 localStorage.setItem('authToken', token);
 window.location.reload();
 };

 const logout = () => {
 localStorage.removeItem('authToken');
 setSession(null);
 };

 return (
 <SessionContext.Provider value={{ session, loading, login, logout }}>
 {children}
 </SessionContext.Provider>
 );
};