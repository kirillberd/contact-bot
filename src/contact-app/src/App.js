import { React, useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import AddContactForm from './components/AddContactForm';
import SearchContactsForm from './components/SearchContactsForm';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import LoginForm from './components/LoginForm';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return localStorage.getItem('isAuthenticated') === 'true';
  });

  useEffect(() => {
    const checkAuth = () => {
      const authStatus = localStorage.getItem('isAuthenticated') === 'true';
      setIsAuthenticated(authStatus);
    };
    
    checkAuth();
    
    window.addEventListener('storage', checkAuth);
    
    return () => window.removeEventListener('storage', checkAuth);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('isAuthenticated');
    setIsAuthenticated(false);
  };

  return (
    <Router>
      <div>
        <Navbar isAuthenticated={isAuthenticated} onLogout={handleLogout} />
        <div className="container">
          <Routes>
            <Route
              path="/contact-bot"
              element={
                <ProtectedRoute>
                  <AddContactForm />
                </ProtectedRoute>
              }
            />
            <Route
              path="/contact-bot/search-contacts"
              element={
                <ProtectedRoute>
                  <SearchContactsForm />
                </ProtectedRoute>
              }
            />
            <Route path="/login" element={<LoginForm setIsAuthenticated={setIsAuthenticated} />} />
            <Route path="/" element={<Navigate to="/contact-bot" replace />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;