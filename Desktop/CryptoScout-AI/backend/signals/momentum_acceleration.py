
# backend/signals/momentum_acceleration.py

from typing import List, Dict


def detect_momentum_acceleration(projects: List[Dict]) -> List[Dict]:
    """
    Detect coins where short-term momentum is increasing
    faster than the longer-term trend.
    """

    signals = []

    for p in projects:

        change_24h = float(p.get("price_change_24h") or 0)
        change_7d = float(p.get("price_change_7d") or 0)
        volume = float(p.get("volume_24h") or 0)
        ai_score = float(p.get("ai_score") or 0)

        # approximate daily average from 7d trend
        avg_daily_trend = change_7d / 7

        acceleration = change_24h - avg_daily_trend

        if (
            acceleration > 3 and
            volume > 2_000_000 and
            ai_score > 65
        ):

            signals.append({
                "type": "MOMENTUM_ACCELERATION",
                "symbol": p.get("symbol"),
                "name": p.get("name"),
                "change_24h": change_24h,
                "change_7d": change_7d,
                "acceleration": round(acceleration, 2),
                "ai_score": ai_score
            })

    return signals