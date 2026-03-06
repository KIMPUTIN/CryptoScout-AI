
import { useAuth } from "../context/AuthContext";
import { useUsage } from "../hooks/useUsage";

function Sidebar({ activeView, setActiveView, collapsed, setCollapsed }) {
    const { user, logout } = useAuth();
    const { usage } = useUsage();

    const navItems = [
        { id: "discover", icon: "🔍", label: "Discover" },
        { id: "watchlist", icon: "⭐", label: "Watchlist" },
        { id: "portfolio", icon: "📊", label: "Portfolio" },
        { id: "analytics", icon: "📈", label: "Analytics" }
    ];

    return (
        <div style={{
            width: collapsed ? "80px" : "260px",
            background: "#0f172a",
            borderRight: "1px solid #1f2937",
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            transition: "width 0.2s"
        }}>

            {/* =======================
               HEADER
            ======================= */}

            <div>

                <div style={{
                    padding: "20px",
                    borderBottom: "1px solid #1f2937",
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center"
                }}>
                    {!collapsed && (
                        <h2 style={{
                            color: "#e2e8f0",
                            fontSize: "1.2rem"
                        }}>
                            CryptoScout AI
                        </h2>
                    )}

                    <button
                        onClick={() => setCollapsed(!collapsed)}
                        style={toggleBtn}
                    >
                        {collapsed ? "→" : "←"}
                    </button>
                </div>

                {/* =======================
                   NAVIGATION
                ======================= */}

                <div style={{ padding: "12px" }}>
                    {navItems.map(item => (
                        <div
                            key={item.id}
                            onClick={() => setActiveView(item.id)}
                            style={{
                                ...navItem,
                                background:
                                    activeView === item.id
                                        ? "#1f2937"
                                        : "transparent"
                            }}
                        >
                            <span>{item.icon}</span>

                            {!collapsed && (
                                <span>{item.label}</span>
                            )}
                        </div>
                    ))}
                </div>

                {/* =======================
                   USAGE METER
                ======================= */}

                {!collapsed && usage && (
                    <div style={{
                        padding: "16px",
                        margin: "10px",
                        background: "#1f2937",
                        borderRadius: "8px"
                    }}>

                        <div style={{
                            fontSize: "0.8rem",
                            color: "#9ca3af"
                        }}>
                            AI Analyses Today
                        </div>

                        {usage.limit ? (
                            <>
                                <strong>
                                    {usage.used} / {usage.limit}
                                </strong>

                                <div style={progressBar}>
                                    <div
                                        style={{
                                            ...progressFill,
                                            width: `${(usage.used / usage.limit) * 100}%`
                                        }}
                                    />
                                </div>
                            </>
                        ) : (
                            <strong style={{ color: "#4ade80" }}>
                                Unlimited
                            </strong>
                        )}

                    </div>
                )}

            </div>

            {/* =======================
               USER SECTION
            ======================= */}

            <div style={{
                padding: "16px",
                borderTop: "1px solid #1f2937"
            }}>

                {!collapsed && user && (
                    <div style={{ marginBottom: "10px" }}>

                        <div style={{
                            color: "#e5e7eb",
                            fontWeight: "600"
                        }}>
                            {user.name || "User"}
                        </div>

                        <div style={{
                            fontSize: "0.8rem",
                            color: "#9ca3af"
                        }}>
                            Plan: {user.plan || "Free"}
                        </div>

                    </div>
                )}

                <button
                    onClick={logout}
                    style={logoutBtn}
                >
                    {collapsed ? "🚪" : "Logout"}
                </button>

            </div>

        </div>
    );
}

export default Sidebar;

const navItem = {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    padding: "10px",
    borderRadius: "6px",
    cursor: "pointer",
    color: "#e5e7eb",
    marginBottom: "6px"
};

const toggleBtn = {
    background: "transparent",
    border: "1px solid #374151",
    color: "#9ca3af",
    borderRadius: "6px",
    padding: "4px 8px",
    cursor: "pointer"
};

const logoutBtn = {
    width: "100%",
    padding: "8px",
    background: "#374151",
    border: "none",
    borderRadius: "6px",
    color: "#e5e7eb",
    cursor: "pointer"
};

const progressBar = {
    height: "6px",
    background: "#374151",
    borderRadius: "4px",
    marginTop: "6px",
    overflow: "hidden"
};

const progressFill = {
    height: "100%",
    background: "#6366f1"
};