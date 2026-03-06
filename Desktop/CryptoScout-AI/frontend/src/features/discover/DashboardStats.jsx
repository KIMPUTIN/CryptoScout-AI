
function DashboardStats({ projects }) {
    const total = projects.length;
    const avg =
        projects.reduce((a, p) => a + (p.ai_score || 0), 0) /
            total || 0;

    const buys = projects.filter(p => p.ai_verdict === "BUY").length;

    return (
        <div style={{ marginBottom: "32px" }}>
            <div>Total Projects: {total}</div>
            <div>Avg AI Score: {avg.toFixed(1)}</div>
            <div>Buy Signals: {buys}</div>
        </div>
    );
}

export default DashboardStats;