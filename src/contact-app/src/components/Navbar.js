import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = ({ isAuthenticated, onLogout }) => {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container">
        
        {isAuthenticated && (
          <div className="collapse navbar-collapse">
            <ul className="navbar-nav me-auto">
              <li className="nav-item">
                <Link className="nav-link" to="/contact-bot">Add Contacts</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/contact-bot/search-contacts">Search Contacts</Link>
              </li>
              <li className='nav-item'>

              <button 
              onClick={onLogout}
              style={{
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                padding: 0,
                font: 'inherit',
                color: 'inherit'
              }}
            >
              Logout
            </button>
              </li>
            </ul>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;