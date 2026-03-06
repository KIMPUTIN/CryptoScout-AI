
import DashboardStats from "./DashboardStats";
import CategoryFilters from "./CategoryFilters";
import ProjectCard from "./ProjectCard";

function DiscoverView({
    projects,
    loading,
    error,
    category,
    setCategory,
    watchlist,
    toggleWatchlist,
    explanations,
    explain,
    analyze,
    analysisResults
}) {
    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <>
            <DashboardStats projects={projects} />

            <CategoryFilters
                category={category}
                setCategory={setCategory}
            />

            <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(350px, 1fr))",
                gap: "24px"
            }}>
                {projects.map(project => (
                    <ProjectCard
                        key={project.symbol}
                        project={project}
                        isInWatchlist={watchlist.some(w => w.symbol === project.symbol)}
                        toggleWatchlist={toggleWatchlist}
                        explanations={explanations}
                        explain={explain}
                        analyze={analyze}
                        analysisResults={analysisResults}
                    />
                ))}
            </div>
        </>
    );
}

export default DiscoverView;