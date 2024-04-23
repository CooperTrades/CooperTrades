import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './trade.css'; // Make sure the path matches your file structure

function Trade() {
    const [items, setItems] = useState([]);

    useEffect(() => {
        fetchAvailableItems();
    }, []);

    const fetchAvailableItems = async () => {
        try {
            const response = await axios.get('http://localhost:6543/items/available'); // Endpoint to get available items
            setItems(response.data);
        } catch (error) {
            console.error('Error fetching available items:', error);
        }
    };

    return (
        <div className="trade-container">
            <h1>Items Up for Trade</h1>
            <ul>
                {items.map(item => (
                    <li key={item.item_id}>
                        <div>Description: {item.description}</div>
                        <div>Category: {item.category}</div>
                        <div>Condition: {item.condition}</div>
                        <div>User ID: {item.user_id} (Username: {item.username})</div>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Trade;
