
# backend/signals/breakout.py

from typing import List, Dict


def detect_breakouts(projects: List[Dict]) -> List[Dict]:
    """
    Detect breakout momentum signals.
    """

    signals = []

    for p in projects:

        change_24h = float(p.get("price_change_24h") or 0)
        volume = float(p.get("volume_24h") or 0)
        ai_score = float(p.get("ai_score") or 0)

        # breakout conditions
        if change_24h > 10 and volume > 5_000_000 and ai_score > 70:

            signals.append({
                "type": "BREAKOUT",
                "symbol": p.get("symbol"),
                "name": p.get("name"),
                "ai_score": ai_score,
                "change_24h": change_24h,
                "volume_24h": volume
            })

    return signals