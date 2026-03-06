
function WatchlistView({ watchlist }) {
    if (!watchlist.length) {
        return <div>Your watchlist is empty.</div>;
    }

    return (
        <div>
            {watchlist.map(item => (
                <div key={item.symbol}>
                    {item.name} ({item.symbol})
                </div>
            ))}
        </div>
    );
}

export default WatchlistView;