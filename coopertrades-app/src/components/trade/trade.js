import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { UserContext } from '../UserContext';
import './trade.css';

function Trade() {
    const [myItems, setMyItems] = useState([]);
    const [otherItems, setOtherItems] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [selectedItemForTrade, setSelectedItemForTrade] = useState(null);
    const { user } = useContext(UserContext);

    useEffect(() => {
        fetchItems();
    }, [user]); // Refetch when user changes

    const fetchItems = async () => {
        try {
            const response = await axios.get('http://localhost:6543/items');
            const availableItems = response.data || [];
            const myAvailableItems = availableItems.filter(item => item.user_id === user.user_id && item.trade_status === "AVAILABLE");
            const otherAvailableItems = availableItems.filter(item => item.user_id !== user.user_id && item.trade_status === "AVAILABLE");
            setMyItems(myAvailableItems);
            setOtherItems(otherAvailableItems);
        } catch (error) {
            console.error('Error fetching available items:', error);
        }
    };

    const handleTradeInitiation = (accepterItemId) => {
        console.log("accepterItemId", accepterItemId);
        setShowModal(true);
        setSelectedItemForTrade(accepterItemId);
    };

    const confirmTrade = async (requesterItemId) => {
        try {
            console.log("requesterItemId:", requesterItemId);
            console.log("selectedItemForTrade:", selectedItemForTrade);
    
            const response = await axios.post('http://localhost:6543/trade/execute', {
                requester_item_id: requesterItemId,
                accepter_item_id: selectedItemForTrade
            });
    
            alert(response.data.message || 'Trade initiated successfully!');
            setShowModal(false);
            fetchItems();  // Refresh items list
        } catch (error) {
            console.error('Error initiating trade:', error);
            alert('Failed to initiate trade');
        }
    };
    

    return (
        <div className="trade-container">
            {showModal && (
                <div className="modal">
                    <h2>Select an Item to Trade</h2>
                    <ul>
                        {myItems.map(item => (
                            <li key={item.item_id}>
                                <div>Description: {item.description}</div>
                                <button onClick={() => confirmTrade(item.user_id)}>Select for Trade</button>
                            </li>
                        ))}
                    </ul>
                    <button onClick={() => setShowModal(false)}>Close</button>
                </div>
            )}
            <div className="trade-columns">
                <div className="trade-column">
                    <h2>My Items</h2>
                    <ul>
                        {myItems.map(item => (
                            <li key={item.item_id}>
                                <div>Description: {item.description}</div>
                                <div>Category: {item.category}</div>
                                <div>Condition: {item.condition}</div>
                            </li>
                        ))}
                    </ul>
                </div>
                <div className="trade-column">
                    <h2>Other Items</h2>
                    <ul>
                        {otherItems.map(item => (
                            <li key={item.item_id}>
                                <div>Description: {item.description}</div>
                                <div>Category: {item.category}</div>
                                <div>Condition: {item.condition}</div>
                                <button onClick={() => handleTradeInitiation(item.user_id)}>Initiate Trade</button>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default Trade;
