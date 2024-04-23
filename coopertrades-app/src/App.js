//import React, { useState, useEffect } from 'react';
//import axios from 'axios';
//import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
//import AddItem from './components/item/addItem'; // Import the AddItem component
//import CreateUser from './components/user/CreateUser'; // Import the CreateUser component
//import './App.css';
//
//function App() {
//    const [items, setItems] = useState([]);
//
//    useEffect(() => {
//        fetchItems();
//    }, []);
//
//    async function fetchItems() {
//        try {
//            const response = await axios.get('http://localhost:6543/items');
//            setItems(response.data);
//        } catch (error) {
//            console.error('There was an error fetching the items:', error);
//        }
//    }
//
//    return (
//        <Router>
//            <div className="App">
//                <h1>Item Management</h1>
//                <nav>
//                    <Link to="/">Home</Link> | <Link to="/create-user">Create User</Link>
//                </nav>
//                <Routes>
//                    <Route path="/" element={
//                        <>
//                            <AddItem onItemAdded={fetchItems} />
//                            <h2>Items</h2>
//                            <ul>
//                                {items.map(item => (
//                                    <li key={item.id}>{`${item.description} (Category: ${item.category}, Condition: ${item.condition})`}</li>
//                                ))}
//                            </ul>
//                        </>
//                    } />
//                    <Route path="/create-user" element={<CreateUser />} />
//                    {/* Additional paths can be added below using similar pattern */}
//                </Routes>
//            </div>
//        </Router>
//    );
//}
//
//export default App;
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import AddItem from './components/item/addItem'; // Import the AddItem component
import CreateUser from './components/user/CreateUser'; // Import the CreateUser component
import Login from './components/login/login'; // Import the Login component
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
        <Router>
            <div className="App">
                <h1>Item Management</h1>
                <nav>
                    <Link to="/">Home</Link> | <Link to="/create-user">Create User</Link> | <Link to="/login">Login</Link>
                </nav>
                <Routes>
                    <Route path="/" element={
                        <>
                            <AddItem onItemAdded={fetchItems} />
                            <h2>Items</h2>
                            <ul>
                                {items.map(item => (
                                    <li key={item.id}>{`${item.description} (Category: ${item.category}, Condition: ${item.condition})`}</li>
                                ))}
                            </ul>
                        </>
                    } />
                    <Route path="/create-user" element={<CreateUser />} />
                    <Route path="/login" element={<Login />} />  // Add this line for the Login route
                </Routes>
            </div>
        </Router>
    );
}

export default App;

