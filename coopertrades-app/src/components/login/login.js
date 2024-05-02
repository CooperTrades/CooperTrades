import React, { useState } from 'react';
import axios from 'axios';
import { useUser } from '../UserContext'; // Import useUser
import './login.css';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { login } = useUser(); // Use the login function from context

    const handleLogin = async (e) => {
        e.preventDefault();
        setError(''); // Clear previous errors

        try {
            const response = await axios.post('http://localhost:6543/login', {
                username,
                password
            });

            if (response.data.user_id) {
                console.log("id: ", response.data.user_id);
                login(response.data); // Update the user context
                alert("Login successful!");
                // Redirect to another page or update UI
            } else {
                throw new Error('Invalid username or password');
            }
        } catch (err) {
            setError('Invalid username or password');
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
