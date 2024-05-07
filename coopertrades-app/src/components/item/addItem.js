import React, { useState, useContext } from 'react';
import axios from 'axios';
import { UserContext } from '../UserContext'; // Update this path according to your project structure
import './addItem.css';

function AddItem({ onItemAdded }) {
    const { user } = useContext(UserContext); // Access the user context

    const [formData, setFormData] = useState({
        description: '',
        category: '',
        condition: '',
        user_id: user ? user.user_id : '',
        trade_status: 'AVAILABLE',
    });

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData(prevFormData => ({
            ...prevFormData,
            [name]: value,
        }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!user) {
            alert("You must be logged in to add items.");
            return;
        }
        try {
            const jsonFormData = JSON.stringify(formData);
            const config = {
                headers: {
                    'Content-Type': 'application/json'
                }
            };
            const response = await axios.post('http://localhost:6543/items/add', jsonFormData, config);
            console.log('Server response:', response.data);
            onItemAdded();
            setFormData({ description: '', category: '', condition: '', user_id: user ? user.user_id : '', trade_status: 'AVAILABLE' });
        } catch (error) {
            console.error('There was an error adding the item:', error);
        }
    };

    if (!user) {
        return (
            <div className="addItemForm">
                <h2>Add Item</h2>
                <p>You must be logged in to add an item. Please log in and try again.</p>
            </div>
        );
    }

    return (
        <div className="addItemForm">
            <h2>Add Item</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    Description: <input type="text" name="description" value={formData.description} onChange={handleChange} required />
                </div>
                <div>
                    Category:
                    <select name="category" value={formData.category} onChange={handleChange} required>
                        <option value="ART">Art</option>
                        <option value="CLOTHING">Clothing</option>
                        <option value="MISC">Misc</option>
                    </select>
                </div>
                <div>
                    Condition:
                    <select name="condition" value={formData.condition} onChange={handleChange} required>
                        <option value="NEW">New</option>
                        <option value="USED">Used</option>
                        <option value="OLD">Old</option>
                    </select>
                </div>
                <div>
                    Trade Status:
                    <select name="trade_status" value={formData.trade_status} onChange={handleChange} required>
                        <option value="AVAILABLE">Available</option>
                        <option value="PENDING">Pending</option>
                        <option value="NOT_AVAILABLE">Not Available</option>
                    </select>
                </div>
                <button type="submit">Add Item</button>
            </form>
        </div>
    );
}

export default AddItem;
