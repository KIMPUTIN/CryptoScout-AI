
import { apiClient } from "./apiClient";

export const aiService = {
    analyze: (payload) =>
        apiClient.request("/ai/analyze", {
            method: "POST",
            body: JSON.stringify(payload),
        }),

    explain: (symbol) =>
        apiClient.request(`/ai/explain/${symbol}`, {
            method: "GET",
        }),
};