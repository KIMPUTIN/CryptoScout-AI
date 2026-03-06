
import { useEffect, useState } from "react";
import { watchlistService } from "../api/watchlistService";

export function useWatchlist(isAuthenticated) {
    const [watchlist, setWatchlist] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!isAuthenticated) {
            setWatchlist([]);
            return;
        }

        let isMounted = true;

        setLoading(true);
        setError(null);

        watchlistService
            .get()
            .then((data) => {
                if (isMounted) setWatchlist(data);
            })
            .catch((err) => {
                if (isMounted) {
                    setError("Failed to load watchlist");
                    console.error(err);
                }
            })
            .finally(() => {
                if (isMounted) setLoading(false);
            });

        return () => {
            isMounted = false;
        };
    }, [isAuthenticated]);

    const toggle = async (symbol) => {
        try {
            const exists = watchlist.some((i) => i.symbol === symbol);

            await watchlistService.toggle(symbol, exists);

            // Optimistic update (no second GET call)
            setWatchlist((prev) =>
                exists
                    ? prev.filter((i) => i.symbol !== symbol)
                    : [...prev, { symbol }]
            );

        } catch (err) {
            console.error(err);
        }
    };

    return { watchlist, toggle, loading, error };
}