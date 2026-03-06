
export default function AnalysisPanel({ analysis }) {
    if (!analysis) return null;

    const {
        symbol,
        ai_score,
        verdict,
        momentum,
        volatility,
        liquidity,
        recommendation,
    } = analysis;

    return (
        <div style={{
            marginTop: "16px",
            background: "#111827",
            padding: "16px",
            borderRadius: "10px",
            border: "1px solid #374151"
        }}>
            <h4 style={{ marginBottom: "10px" }}>
                🤖 AI Analysis: {symbol}
            </h4>

            <div style={{
                display: "flex",
                gap: "20px",
                marginBottom: "10px"
            }}>
                <strong>Score: {ai_score}</strong>
                <strong>Verdict: {verdict}</strong>
            </div>

            <div style={{ fontSize: "0.9rem", color: "#9ca3af" }}>
                <div>Momentum: {momentum}</div>
                <div>Volatility: {volatility}</div>
                <div>Liquidity: {liquidity}</div>
            </div>

            <div style={{
                marginTop: "12px",
                padding: "10px",
                background: "#1f2937",
                borderRadius: "6px"
            }}>
                {recommendation}
            </div>
        </div>
    );
}