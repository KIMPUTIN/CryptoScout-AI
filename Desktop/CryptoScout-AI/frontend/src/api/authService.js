
import { apiClient } from "./apiClient";

export const authService = {
    googleLogin: (token) =>
        apiClient.request("/auth/google", {
            method: "POST",
            body: JSON.stringify({ token }),
        }),
};