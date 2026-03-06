
// src/layout/ProtectedRoute.jsx

export default function ProtectedRoute({ children, requiredRole }) {
    const { user, isAuthenticated } = useAuth();

    if (!isAuthenticated) {
        return <Navigate to="/" replace />;
    }

    if (requiredRole && user.role !== requiredRole) {
        return <div>Unauthorized</div>;
    }

    return children;
}