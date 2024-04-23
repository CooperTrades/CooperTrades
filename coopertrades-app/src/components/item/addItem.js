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
   // Use JSON.stringify to convert formData to a JSON string
   const jsonFormData = JSON.stringify(formData);

   // Include the Content-Type header
   const config = {
     headers: {
       'Content-Type': 'application/json'
     }
   };

   // Pass jsonFormData and config to axios.post
   await axios.post('http://localhost:6543/items/add', jsonFormData, config);
   onItemAdded(); // Notify the parent component to refresh the item list
   setFormData({ description: '', category: '', condition: '', user_id: '' }); // Reset form fields
 } catch (error) {
   console.error('There was an error adding the item:', error);
 }
};
// const handleSubmit = async (event) => {
//   event.preventDefault();
//   try {
//     // Convert formData to URL-encoded string
//     const formBody = Object.keys(formData).map(key => encodeURIComponent(key) + '=' + encodeURIComponent(formData[key])).join('&');
//
//     // Include the Content-Type header for URL-encoded form data
//     const config = {
//       headers: {
//         'Content-Type': 'application/x-www-form-urlencoded'
//       }
//     };
//
//     // Pass formBody and config to axios.post
//     await axios.post('http://localhost:6543/items/add', formBody, config);
//     onItemAdded(); // Notify the parent component to refresh the item list
//     setFormData({ description: '', category: '', condition: '', user_id: '' }); // Reset form fields
//   } catch (error) {
//     console.error('There was an error adding the item:', error);
//   }
// };


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
