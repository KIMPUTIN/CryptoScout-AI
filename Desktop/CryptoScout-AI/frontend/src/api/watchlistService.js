
import { apiClient } from "./apiClient";

export const watchlistService = {
    get: () => apiClient.request("/watchlist/"),

    toggle: (symbol, exists) =>
        apiClient.request(`/watchlist/${exists ? "remove" : "add"}/${symbol}`, {
            method: "POST",
        }),
};