
import { BrowserRouter, Routes, Route } from "react-router-dom";

import ProtectedRoute from "./layout/ProtectedRoute";
import RequirePlan from "./layout/RequirePlan";

import Home from "./pages/Home";
import { Suspense, lazy } from "react";

const MonitoringDashboard = lazy(() =>
  import("./features/monitoring/MonitoringDashboard")
);

function App() {
    return (
        <BrowserRouter>
            <Routes>

                {/* Main app */}
                <Route path="/" element={<Home />} />

                {/* Admin monitor */}
                <Route
                    path="/monitor"
                    element={
                        <ProtectedRoute>
                            <RequirePlan plan="admin">
                                <Suspense fallback={<div>Loading...</div>}>
                                    <MonitoringDashboard />
                                </Suspense>
                            </RequirePlan>
                        </ProtectedRoute>
                    }
                />

            </Routes>
        </BrowserRouter>
    );
}

export default App;