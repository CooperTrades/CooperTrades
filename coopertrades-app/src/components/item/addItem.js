import React, { useState } from 'react';
import axios from 'axios';
import './addItem.css'; // Import the CSS file for styling

function AddItem({ onItemAdded }) {
    const [formData, setFormData] = useState({
        description: '',
        category: '',
        condition: '',
        user_id: '',
        trade_status: 'AVAILABLE', // Default to 'AVAILABLE'
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
        try {
            // Use JSON.stringify to convert formData to a JSON string
            const jsonFormData = JSON.stringify(formData);

            // Include the Content-Type header
            const config = {
                headers: {
                    'Content-Type': 'application/json'
                }
            };

            // Pass jsonFormData and config to axios.post
            const response = await axios.post('http://localhost:6543/items/add', jsonFormData, config);
            console.log('Server response:', response.data);
            onItemAdded(); // Notify the parent component to refresh the item list
            setFormData({ description: '', category: '', condition: '', user_id: '', trade_status: 'AVAILABLE' }); // Reset form fields
        } catch (error) {
            console.error('There was an error adding the item:', error);
        }
    };

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
                    User ID: <input type="number" name="user_id" value={formData.user_id} onChange={handleChange} required />
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
