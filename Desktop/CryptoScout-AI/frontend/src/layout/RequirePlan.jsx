
import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import UpgradeModal from "../features/billing/UpgradeModal";

export default function RequirePlan({ plan, children }) {
    const { hasPlan } = useAuth();
    const [showUpgrade, setShowUpgrade] = useState(false);

    if (!hasPlan(plan)) {
        return (
            <>
                <button
                    onClick={() => setShowUpgrade(true)}
                    style={{
                        background: "#374151",
                        border: "none",
                        padding: "0.5rem 1rem",
                        borderRadius: "6px",
                        color: "#9ca3af",
                        cursor: "pointer"
                    }}
                >
                    🔒 Pro Feature
                </button>

                {showUpgrade && (
                    <UpgradeModal
                        onClose={() => setShowUpgrade(false)}
                    />
                )}
            </>
        );
    }

    return children;
}