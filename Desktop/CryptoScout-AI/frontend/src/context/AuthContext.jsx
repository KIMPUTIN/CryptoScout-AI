
import { createContext, useContext, useEffect, useState } from "react";



const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);

    useEffect(() => {
        try {
            const savedUser = localStorage.getItem("user");
            const token = localStorage.getItem("token");

            if (savedUser && token) {
                setUser(JSON.parse(savedUser));
            } else {
                localStorage.removeItem("user");
                localStorage.removeItem("token");
            }
        } catch {
            localStorage.removeItem("user");
            localStorage.removeItem("token");
        }
    }, []);

    const login = (userData, token) => {
        localStorage.setItem("user", JSON.stringify(userData));
        localStorage.setItem("token", token);
        setUser(userData);
    };

    const logout = () => {
        localStorage.removeItem("user");
        localStorage.removeItem("token");
        setUser(null);
    };

    const isAuthenticated = !!user;

    const hasPlan = (requiredPlan) => {
        if (!user?.plan) return false;

        const hierarchy = {
            free: 0,
            pro: 1,
            trader: 2,
            admin: 3,
        };

        return hierarchy[user.plan] >= hierarchy[requiredPlan];
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                isAuthenticated,
                login,
                logout,
                hasPlan,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => {
    const context = useContext(AuthContext);

    if (!context) {
        throw new Error("useAuth must be used within an AuthProvider");
    }

    return context;
};