import React, {useContext} from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import {UserContext, UserProvider, useUser} from './components/UserContext';
import AddItem from './components/item/addItem';
import CreateUser from './components/user/CreateUser';
import Login from './components/login/login';
import Trade from './components/trade/trade';
import Profile from './components/profile/profile';
import './App.css';

function App() {
    const [items, setItems] = React.useState([]);
    const userData = useContext(UserContext);  // Access the context

    const user = userData ? userData.user : null;  // Check null

    React.useEffect(() => {
        fetchItems();
    }, []);

    async function fetchItems() {
        try {
            const response = await axios.get('http://localhost:6543/items');
            setItems(response.data);
        } catch (error) {
            console.error('Error fetching items:', error);
        }
    }

    return (
        <UserProvider>
            <Router>
                <div className="App">
                    <h1>CooperTrades</h1>
                    <div className="user-id">
                        {user ? `User ID: ${user.user_id}` : "Not logged in"}
                    </div>
                    <nav>
                        <Link to="/">Home</Link> |
                        <Link to="/create-user">Create User</Link> |
                        <Link to="/login">Login</Link> |
                        <Link to="/trades">View Trades</Link> |
                        <Link to="/profile">View Profile</Link>
                    </nav>
                    <Routes>
                        <Route path="/" element={
                            <>
                                <AddItem onItemAdded={fetchItems}/>
                                <h2>Items</h2>
                                <ul>
                                    {items.map(item => (
                                        <li key={item.id}>{`${item.description} (Category: ${item.category}, Condition: ${item.condition})`}</li>
                                    ))}
                                </ul>
                            </>
                        }/>
                        <Route path="/create-user" element={<CreateUser/>}/>
                        <Route path="/login" element={<Login/>}/>
                        <Route path="/trades" element={<Trade/>}/>
                        <Route path="/profile" element={<Profile/>}/>
                    </Routes>
                </div>
            </Router>
        </UserProvider>
    );
}

export default App;

