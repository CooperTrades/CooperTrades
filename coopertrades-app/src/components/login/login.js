import React, { useState } from 'react';
import axios from 'axios';
import './login.css';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        setError(''); // Clear previous errors

        try {
            const response = await axios.post('http://localhost:6543/login', {
                username,
                password
            });

            // Check if login was successful based on the response
            if (response.data.user_id) {
                alert("Login successful!");
                // Redirect user or do something upon success
                // Example: Redirect to another page or update the global state
            } else {
                throw new Error('Invalid username or password'); // You might not reach here if your server sends errors as 400/500 status codes
            }
        } catch (err) {
            if (err.response && err.response.data) {
                // The server responded with a status outside the range of 2xx and error details
                setError(err.response.data.error || 'Invalid username or password');
            } else {
                // Something happened in setting up the request that triggered an Error
                setError('Network error, please try again.');
            }
        }
    };

    return (
        <div className="login-container">
            <form className="login-form" onSubmit={handleLogin}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="input-field"
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="input-field"
                    required
                />
                {error && <div className="error-message">{error}</div>}
                <button type="submit" className="submit-button">Login</button>
            </form>
        </div>
    );
}

export default Login;
