
# backend/signals/gem_detector.py

from typing import List, Dict


def detect_hidden_gems(projects: List[Dict]) -> List[Dict]:
    """
    Detect small-cap high momentum coins.
    """

    gems = []

    for p in projects:

        market_cap = float(p.get("market_cap") or 0)
        change_7d = float(p.get("price_change_7d") or 0)
        volume = float(p.get("volume_24h") or 0)

        if market_cap < 100_000_000 and change_7d > 15 and volume > 2_000_000:

            gems.append({
                "type": "HIDDEN_GEM",
                "symbol": p.get("symbol"),
                "name": p.get("name"),
                "market_cap": market_cap,
                "change_7d": change_7d
            })

    return gems