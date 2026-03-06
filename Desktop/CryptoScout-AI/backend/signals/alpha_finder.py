
# backend/signals/alpha_finder.py

from typing import List, Dict


def detect_alpha(projects: List[Dict]) -> List[Dict]:
    """
    Detect high-upside alpha opportunities.
    """

    alpha_signals = []

    for p in projects:

        market_cap = float(p.get("market_cap") or 0)
        change_24h = float(p.get("price_change_24h") or 0)
        change_7d = float(p.get("price_change_7d") or 0)
        volume = float(p.get("volume_24h") or 0)
        ai_score = float(p.get("ai_score") or 0)

        # Alpha conditions
        if (
            market_cap < 500_000_000 and
            change_7d > 12 and
            change_24h > 4 and
            volume > 2_000_000 and
            ai_score > 70
        ):

            alpha_signals.append({
                "type": "ALPHA",
                "symbol": p.get("symbol"),
                "name": p.get("name"),
                "market_cap": market_cap,
                "volume_24h": volume,
                "change_24h": change_24h,
                "change_7d": change_7d,
                "ai_score": ai_score
            })

    return alpha_signals