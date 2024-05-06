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

    // State for filtering options
    const [selectedCategory, setSelectedCategory] = useState("");
    const [selectedCondition, setSelectedCondition] = useState("");

    useEffect(() => {
        fetchItems();
    }, [user, selectedCategory, selectedCondition]); // Refetch when user or filter options change

    const fetchItems = async () => {
        try {
            const response = await axios.get('http://localhost:6543/items');
            const availableItems = response.data || [];

            const myAvailableItems = availableItems.filter(item =>
                item.user_id === user.user_id &&
                item.trade_status === "AVAILABLE"
            );

            setMyItems(myAvailableItems);
            const requestBody = {};
            if (selectedCategory) {
                requestBody.category = selectedCategory;
            }
            if (selectedCondition) {
                requestBody.condition = selectedCondition;
            }
            requestBody.user_id = user.user_id;
            const otherAvailableItemsResponse = await axios.post('http://localhost:6543/items/filter', requestBody);
            const otherAvailableItems = otherAvailableItemsResponse.data || [];
            setOtherItems(otherAvailableItems);
        } catch (error) {
            console.error('Error fetching available items:', error);
        }
    };

    const handleTradeInitiation = (accepterItemId) => {
        setShowModal(true);
        setSelectedItemForTrade(accepterItemId);
    };

    const confirmTrade = async (requesterItemId) => {
        try {
            console.log("requesterItemId:", requesterItemId);
            console.log("selectedItemForTrade:", selectedItemForTrade);
            const response = await axios.post('http://localhost:6543/trade/initiate', {
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

            <div className="filter-section">
                <label>
                    Category:
                    <select value={selectedCategory} onChange={e => setSelectedCategory(e.target.value)}>
                        <option value="ALL">All</option>
                        <option value="ART">Art</option>
                        <option value="CLOTHING">Clothing</option>
                        <option value="MISC">Misc</option>
                    </select>
                </label>

                <label>
                    Condition:
                    <select value={selectedCondition} onChange={e => setSelectedCondition(e.target.value)}>
                        <option value="ALL">All</option>
                        <option value="NEW">New</option>
                        <option value="USED">Used</option>
                        <option value="OLD">Old</option>
                    </select>
                </label>
            </div>

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
                                <div>Owner: {item.user_id}</div>
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

