
import { useEffect, useState } from "react";
import { usageService } from "../api/usageService";

export function useUsage() {
    const [usage, setUsage] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        usageService
            .getAnalysisUsage()
            .then(setUsage)
            .catch(console.error)
            .finally(() => setLoading(false));
    }, []);

    return { usage, loading };
}