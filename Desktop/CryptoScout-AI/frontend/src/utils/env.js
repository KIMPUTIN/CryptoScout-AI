
// utils/env.js

export const env = {
    API_URL: import.meta.env.VITE_API_URL,
    GOOGLE_CLIENT_ID: import.meta.env.VITE_GOOGLE_CLIENT_ID,
    IS_PROD: import.meta.env.PROD,
};

export function getApiBaseUrl() {
    if (!env.API_URL) {
        throw new Error("VITE_API_URL is not configured");
    }

    let base = env.API_URL.replace(/\/$/, "");

    if (env.IS_PROD && base.startsWith("http://")) {
        base = base.replace("http://", "https://");
    }

    return base;
}