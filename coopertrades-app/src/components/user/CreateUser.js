import React, { useState } from 'react';
import axios from 'axios';
import './CreateUser.css'; // Import the CSS file for styling

function CreateUser() {
    const [formData, setFormData] = useState({
        email: '',
        username: '',
        password: '',
    });

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData(prevFormData => ({
            ...prevFormData,
            [name]: value
        }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            // Include the Content-Type header
            const config = {
                headers: {
                    'Content-Type': 'application/json'
                }
            };

            // Convert formData to JSON string
            const jsonFormData = JSON.stringify(formData);

            // Send POST request to create user
            await axios.post('http://localhost:6543/users/add', jsonFormData, config);
            alert('User created successfully!');
            setFormData({ email: '', username: '', password: '' }); // Reset form fields after submission
        } catch (error) {
            console.error('Error creating user:', error);
            alert('Failed to create user.');
        }
    };

    return (
        <div className="userForm">
            <h2>Create User</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    Email: <input type="email" name="email" value={formData.email} onChange={handleChange} required />
                </div>
                <div>
                    Username: <input type="text" name="username" value={formData.username} onChange={handleChange} />
                </div>
                <div>
                    Password: <input type="password" name="password" value={formData.password} onChange={handleChange} required />
                </div>
                <button type="submit">Create User</button>
            </form>
        </div>
    );
}

export default CreateUser;
