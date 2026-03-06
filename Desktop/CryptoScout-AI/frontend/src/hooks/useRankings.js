
import { useEffect, useState } from "react";
import { rankingService } from "../api/rankingService";

export function useRankings(category) {
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        let isMounted = true;

        setLoading(true);
        setError(null);

        rankingService
            .get(category)
            .then((data) => {
                if (isMounted) {
                    setProjects(data);
                }
            })
            .catch((err) => {
                if (isMounted) {
                    setError("Failed to load rankings");
                    console.error(err);
                }
            })
            .finally(() => {
                if (isMounted) {
                    setLoading(false);
                }
            });

        return () => {
            isMounted = false;
        };
    }, [category]);

    return { projects, loading, error };
}