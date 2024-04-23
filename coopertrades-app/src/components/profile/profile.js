import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useUser } from '../UserContext'; // Import useUser hook from your context
import './profile.css';

function Profile() {
    const { user } = useUser(); // Access the user object from context
    const [userInfo, setUserInfo] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        if (user) {
            const fetchUserDetails = async () => {
                try {
                    const response = await axios.get(`http://localhost:6543/user/${user.user_id}`);
                    setUserInfo(response.data);
                    setLoading(false);
                } catch (error) {
                    setError('Error fetching user details');
                    setLoading(false);
                }
            };
            fetchUserDetails();
        }
    }, [user]);

    if (!user) return <div>Please log in to view this page.</div>;
    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="profile-container">
            <h1>Profile</h1>
            <div className="user-info">
                <p>Username: {userInfo?.username}</p>
                <p>Email: {userInfo?.email}</p>
            </div>
            <h2>Listed Items</h2>
            <ul>
                {userInfo?.items.map(item => (
                    <li key={item.item_id}>
                        <p>Description: {item.description}</p>
                        <p>Category: {item.category}</p>
                        <p>Condition: {item.condition}</p>
                        <p>Trade Status: {item.trade_status}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Profile;
