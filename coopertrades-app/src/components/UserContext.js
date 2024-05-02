import React, { createContext, useContext, useState } from 'react';

export const UserContext = createContext(null);

export const useUser = () => useContext(UserContext);

export const UserProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [user_id, setuser_id] = useState(null);
    const login = (userData) => {
        setUser(userData);
        setuser_id(userData.user_id);
    };

    const logout = () => {
        setUser(null);
    };

    return (
        <UserContext.Provider value={{ user, login, logout }}>
            {children}
        </UserContext.Provider>
    );
};
