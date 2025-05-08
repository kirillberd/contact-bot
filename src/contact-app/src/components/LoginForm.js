import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";

const LoginForm = ({ setIsAuthenticated }) => {
  const [token, setToken] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const location = useLocation();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (token === process.env.REACT_APP_AUTH_TOKEN) {
      localStorage.setItem('isAuthenticated', 'true');
      setIsAuthenticated(true); // Непосредственное обновление состояния
      const redirectPath = location.state?.from?.pathname || "/contact-bot";
      navigate(redirectPath);
    } else {
      setError("Invalid token");
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h2 className="card-title text-center mb-4">Authorization</h2>
              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label htmlFor="token">Access Token</label>
                  <input
                    type="password"
                    className="form-control"
                    id="token"
                    value={token}
                    onChange={(e) => setToken(e.target.value)}
                    required
                  />
                </div>
                {error && <div className="alert alert-danger mt-2">{error}</div>}
                <button type="submit" className="btn btn-primary btn-block mt-3">
                  Sign In
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;