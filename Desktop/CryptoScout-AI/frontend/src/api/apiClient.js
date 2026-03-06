
// Central transport layer

const getBaseUrl = () => {
    const base = import.meta.env.VITE_API_URL;
    if (!base) throw new Error("API URL not configured");

    if (import.meta.env.PROD && base.startsWith("http://")) {
        return base.replace("http://", "https://").replace(/\/$/, "");
    }

    return base.replace(/\/$/, "");
};

const request = async (endpoint, options = {}) => {
    const token = localStorage.getItem("token");
    const baseUrl = getBaseUrl();

    const res = await fetch(`${baseUrl}${endpoint}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(token && { Authorization: `Bearer ${token}` }),
            ...options.headers,
        },
    });

    if (res.status === 401) {
        localStorage.clear();
        window.location.reload();
    }

    if (!res.ok) {
        let errorData = {};
        try {
            errorData = await res.json();
        } catch {}

        throw {
            status: res.status,
            message: errorData?.detail || "Request failed",
            raw: errorData,
        };
    }

    return res.json();
};

export const apiClient = { request };