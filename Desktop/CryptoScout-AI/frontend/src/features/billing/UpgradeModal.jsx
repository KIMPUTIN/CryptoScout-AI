
import { motion } from "framer-motion";

export default function UpgradeModal({ onClose }) {
    return (
        <div style={overlayStyle}>
            <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                style={modalStyle}
            >
                <h2>🚀 Upgrade to Pro</h2>

                <p style={{ color: "#9ca3af", marginBottom: "1rem" }}>
                    Unlock advanced AI analysis and professional trading insights.
                </p>

                <ul style={featureList}>
                    <li>⚡ Unlimited AI analysis</li>
                    <li>📊 Advanced signal scoring</li>
                    <li>🤖 AI trend predictions</li>
                    <li>📈 Portfolio optimization</li>
                </ul>

                <div style={{ marginTop: "1.5rem", display: "flex", gap: "1rem" }}>
                    <button style={upgradeButton}>
                        Upgrade Now
                    </button>

                    <button style={cancelButton} onClick={onClose}>
                        Maybe Later
                    </button>
                </div>
            </motion.div>
        </div>
    );
}

const overlayStyle = {
    position: "fixed",
    inset: 0,
    background: "rgba(0,0,0,0.6)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    zIndex: 1000
};

const modalStyle = {
    background: "#111827",
    padding: "2rem",
    borderRadius: "12px",
    width: "420px",
    color: "white"
};

const featureList = {
    listStyle: "none",
    padding: 0,
    margin: "1rem 0",
    lineHeight: "1.8"
};

const upgradeButton = {
    background: "#6366f1",
    border: "none",
    padding: "0.6rem 1.2rem",
    borderRadius: "6px",
    color: "white",
    cursor: "pointer"
};

const cancelButton = {
    background: "transparent",
    border: "1px solid #374151",
    padding: "0.6rem 1.2rem",
    borderRadius: "6px",
    color: "#9ca3af",
    cursor: "pointer"
};