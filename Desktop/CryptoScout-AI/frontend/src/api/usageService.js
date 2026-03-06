
import { apiClient } from "./apiClient";

export const usageService = {
    getAnalysisUsage: () =>
        apiClient.request("/usage/analysis"),
};