
import { apiClient } from "./apiClient";

export const rankingService = {
    get: (category) =>
        apiClient.request(`/rankings/${category}`),
};