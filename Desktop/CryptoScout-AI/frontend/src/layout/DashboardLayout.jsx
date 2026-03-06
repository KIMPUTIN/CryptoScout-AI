
import { useState } from "react";
import Sidebar from "./Sidebar";

function DashboardLayout({ children, activeView, setActiveView, user }) {
    const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

    return (
        <div style={{
            display: "flex",
            minHeight: "100vh",
            background: "#0f172a",
            fontFamily: "'Inter', sans-serif",
            color: "#f8fafc"
        }}>
            <Sidebar
                collapsed={sidebarCollapsed}
                setCollapsed={setSidebarCollapsed}
                activeView={activeView}
                setActiveView={setActiveView}
                user={user}
            />

            <div style={{
                flex: 1,
                padding: "32px",
                overflowY: "auto",
                height: "100vh"
            }}>
                {children}
            </div>
        </div>
    );
}

export default DashboardLayout;