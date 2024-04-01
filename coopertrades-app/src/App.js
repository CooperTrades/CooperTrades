import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AddItem from './components/item/addItem'; // Import the AddItem component
import './App.css';

function App() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetchItems();
  }, []);

  async function fetchItems() {
    try {
      const response = await axios.get('http://localhost:6543/items');
      setItems(response.data);
    } catch (error) {
      console.error('There was an error fetching the items:', error);
    }
  }

  return (
    <div className="App">
      <h1>Item Management</h1>
      <AddItem onItemAdded={fetchItems} />
      <h2>Items</h2>
      <ul>
        {items.map(item => (
          <li key={item.id}>{`${item.description} (Category: ${item.category}, Condition: ${item.condition})`}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
