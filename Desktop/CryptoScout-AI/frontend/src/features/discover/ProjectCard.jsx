
import { motion } from "framer-motion";
import RequirePlan from "../../layout/RequirePlan";
import AnalysisPanel from "./AnalysisPanel";

function ProjectCard({
    project,
    isInWatchlist,
    toggleWatchlist,
    explanations,
    explain,
    analyze,
    analysisResults
}) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            style={{
                background: "#1e293b",
                padding: "24px",
                borderRadius: "16px"
            }}
        >
            <h3>{project.name} ({project.symbol})</h3>

            <div style={{ marginTop: "16px", display: "flex", gap: "8px" }}>
                <button onClick={() => explain(project.symbol)}>
                    🧠 Explain
                </button>

                
                <RequirePlan plan="pro">
                    <button
                        onClick={() =>
                            analyze({
                                symbol: project.symbol,
                                portfolio_size: 5000,
                                risk_profile: "balanced",
                                time_horizon: "short-term"
                            })
                        }
                    >
                        🚀 Pro Analyze
                    </button>
                </RequirePlan>

                <button onClick={() => toggleWatchlist(project.symbol)}>
                    {isInWatchlist ? "⭐ Added" : "⭐ Add"}
                </button>
            </div>

            {/* AI Analysis Panel */}
            <AnalysisPanel analysis={analysisResults?.[project.symbol]} />

            {explanations[project.symbol] && (
                <div style={{ marginTop: "12px" }}>
                    {explanations[project.symbol]}
                </div>
            )}

        </motion.div>
    );
}

export default ProjectCard;

