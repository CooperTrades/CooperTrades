import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useUser } from '../UserContext'; // Import useUser hook from your context
import './profile.css';
import {Modal, Button, Form} from 'react-bootstrap'; // Bootstrap's Modal component for creating a modal page

function Profile() {
    const { user } = useUser(); // Access the user object from context
    const [userInfo, setUserInfo] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [showTradesModal, setShowTradesModal] = useState(false); // State to control modal visibility
    const [tradesItems, setTradesItems] = useState([]); // State to store items from trades
    const [selectedTradeItem, setSelectedTradeItem] = useState(null);

    const fetchUserDetails = async () => {
        try {
            const response = await axios.get(`http://localhost:6543/user/${user.user_id}`);
            setUserInfo(response.data);
            setLoading(false);
        } catch (error) {
            setError('Error fetching user details');
            setLoading(false);
        }
    };

    useEffect(() => {
        if (user) {

            fetchUserDetails();
        }
    }, [user]);

    const updateTradeStatus = async (itemId, newStatus) => {
        try {
            const response = await axios.post(`http://localhost:6543/item/update-status`, {
                item_id: itemId,
                trade_status: newStatus
            });
            if (response.status === 200) {
                alert("Trade status updated successfully.");
                fetchUserDetails(); // Refresh user details to reflect the updated trade status
            } else {
                alert("Failed to update trade status.");
            }
        } catch (error) {
            console.error('Error updating trade status:', error);
            alert("Error updating trade status.");
        }
    };

    const fetchTradesItems = async () => {
        try {
            const response = await axios.post(`http://localhost:6543/trades/accepter`, { accepter_id: user.user_id });
            setTradesItems(response.data.requester_items);
            setShowTradesModal(true); // Show the modal with fetched items
        } catch (error) {
            alert("Error fetching trades.");
        }
    };

    // const executeTrade = async (item_id) => {
    //     try {
    //         const response = await axios.post(`http://localhost:6543/trade/execute`, {
    //             accepter_item_id: item_id, requester_item_id: tradesItems[0].item_id });
    //
    //         alert("Trade executed successfully.");
    //     } catch (error) {
    //         alert("Error executing trade.");
    //     }
    // };
    const executeTrade = async (item_id) => {
        if (!selectedTradeItem) {
            alert("Please select an item to trade.");
            return;
        }
        try {
            const response = await axios.post(`http://localhost:6543/trade/execute`, {
                accepter_item_id: item_id,
                requester_item_id: selectedTradeItem
                // requester_item_id: tradesItems[0].item_id
            });
            alert("Trade executed successfully.");
            setShowTradesModal(false);
            resetOtherItemsStatus();
            fetchUserDetails();
        } catch (error) {
            alert("Error executing trade.");
        }
    };

    const resetOtherItemsStatus = async () => {
        const updates = tradesItems.filter(item => item.item_id !== selectedTradeItem)
            .map(item => {
                return axios.post(`http://localhost:6543/item/update-status`, {
                    item_id: item.item_id,
                    trade_status: 'AVAILABLE'
                });
            });

        try {
            await Promise.all(updates); // Execute all updates at once
            console.log('All other items have been reset to AVAILABLE.');
        } catch (error) {
            console.error('Error resetting other items:', error);
        }
    };

    if (!user) return <div>Please log in to view this page.</div>;
    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="profile-container">
            <h1>Profile</h1>
            <div className="user-info">
                <p>Username: {userInfo?.username}</p>
                <p>Email: {userInfo?.email}</p>
            </div>
            <h2>Listed Items</h2>
            <ul>
                {userInfo?.items.map(item => (
                    <li key={item.item_id}>
                        <p>Description: {item.description}</p>
                        <p>Category: {item.category}</p>
                        <p>Condition: {item.condition}</p>
                        <p>Trade Status: {item.trade_status}</p>
                        {item.trade_status !== "NOT_AVAILABLE" && item.trade_status !== "PENDING" && (
                            <button onClick={() => updateTradeStatus(item.item_id, 'NOT_AVAILABLE')}>
                                Mark as Not Available
                            </button>
                        )}
                        {item.trade_status !== "AVAILABLE" && item.trade_status !== "PENDING" && (
                            <button onClick={() => updateTradeStatus(item.item_id, 'AVAILABLE')}>
                                Mark as Available
                            </button>
                        )}
                        {item.trade_status === "PENDING" && (
                            <button onClick={() => executeTrade(item.item_id)}>
                                Execute Trade
                            </button>
                        )}
                    </li>
                ))}
            </ul>
            <button onClick={fetchTradesItems}>View Trade Items</button>
            <Modal show={showTradesModal} onHide={() => setShowTradesModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Select an Item to Trade</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        {tradesItems.map((item) => (
                            <Form.Check
                                type="radio"
                                id={`trade-item-${item.item_id}`}
                                label={`${item.description} - ${item.category}`}
                                name="tradeItem"
                                onChange={() => setSelectedTradeItem(item.item_id)}
                            />
                        ))}
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowTradesModal(false)}>Close</Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
}

export default Profile;