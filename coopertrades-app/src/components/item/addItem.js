import React, { useState } from 'react';
import axios from 'axios';
import './addItem.css';// Import the CSS file for styling

function AddItem({ onItemAdded }) {
  const [formData, setFormData] = useState({
    description: '',
    category: '',
    condition: '',
    user_id: '',
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
      await axios.post('http://localhost:6543/items/add', formData);
      onItemAdded(); // Notify the parent component to refresh the item list
      setFormData({ description: '', category: '', condition: '', user_id: '' }); // Reset form fields
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
          Category: <input type="text" name="category" value={formData.category} onChange={handleChange} required />
        </div>
        <div>
          Condition: <input type="text" name="condition" value={formData.condition} onChange={handleChange} required />
        </div>
        <div>
          User ID: <input type="number" name="user_id" value={formData.user_id} onChange={handleChange} required />
        </div>
        <button type="submit">Add Item</button>
      </form>
    </div>
  );
}

export default AddItem;
