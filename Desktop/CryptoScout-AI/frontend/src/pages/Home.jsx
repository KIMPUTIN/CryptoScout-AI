
import { useState } from "react";

import { useAuth } from "../context/AuthContext";
import { useRankings } from "../hooks/useRankings";
import { useWatchlist } from "../hooks/useWatchlist";
import { useAI } from "../hooks/useAI";

import DashboardLayout from "../layout/DashboardLayout";

import DiscoverView from "../features/discover/DiscoverView";
import WatchlistView from "../features/watchlist/WatchlistView";
import PortfolioView from "../features/portfolio/PortfolioView";
import AnalyticsView from "../features/analytics/AnalyticsView";

function Home() {
    // -----------------------------------
    // Local UI State (Page-level only)
    // -----------------------------------
    const [activeView, setActiveView] = useState("discover");
    const [category, setCategory] = useState("short-term");

    // -----------------------------------
    // Global / Business Hooks
    // -----------------------------------
    const { user, isAuthenticated, logout } = useAuth();

    const { projects, loading, error } = useRankings(category);

    const {
        watchlist,
        toggle: toggleWatchlist,
    } = useWatchlist(isAuthenticated);

    const {
        explanations,
        explain,
        analyze,
        analysisResults
    } = useAI();

    // -----------------------------------
    // View Router
    // -----------------------------------
    const renderView = () => {
        switch (activeView) {
            case "discover":
                return (
                    <DiscoverView
                        projects={projects}
                        loading={loading}
                        error={error}
                        category={category}
                        setCategory={setCategory}
                        watchlist={watchlist}
                        toggleWatchlist={toggleWatchlist}
                        explanations={explanations}
                        explain={explain}
                        analyze={analyze}
                        analysisResults={analysisResults}
                    />
                );

            case "watchlist":
                return (
                    <WatchlistView
                        watchlist={watchlist}
                        toggleWatchlist={toggleWatchlist}
                    />
                );

            case "portfolio":
                return <PortfolioView />;

            case "analytics":
                return <AnalyticsView />;

            default:
                return null;
        }
    };

    // -----------------------------------
    // Layout
    // -----------------------------------
    return (
        <DashboardLayout
            activeView={activeView}
            setActiveView={setActiveView}
            user={user}
            logout={logout}
        >
            {renderView()}
        </DashboardLayout>
    );
}

export default Home;