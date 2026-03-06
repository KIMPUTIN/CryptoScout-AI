
function CategoryFilters({ category, setCategory }) {
    const categories = ["short-term", "long-term", "low-risk", "high-growth"];

    return (
        <div style={{ marginBottom: "24px" }}>
            {categories.map(cat => (
                <button
                    key={cat}
                    onClick={() => setCategory(cat)}
                    style={{
                        marginRight: "10px",
                        background: category === cat ? "#2563eb" : "#1e293b",
                        color: "white"
                    }}
                >
                    {cat}
                </button>
            ))}
        </div>
    );
}

export default CategoryFilters;