
# backend/signals/scoring.py

from typing import Dict


def compute_signal_strength(signal: Dict) -> int:
    """
    Compute signal strength score (0–100)
    """

    base_score = 50

    ai_score = float(signal.get("ai_score") or 0)
    change_24h = float(signal.get("change_24h") or 0)
    volume = float(signal.get("volume_24h") or 0)
    market_cap = float(signal.get("market_cap") or 0)

    score = base_score

    # AI contribution
    score += ai_score * 0.25

    # momentum contribution
    score += min(change_24h * 1.5, 20)

    # liquidity contribution
    if volume > 10_000_000:
        score += 10
    elif volume > 5_000_000:
        score += 5

    # stability bonus
    if market_cap > 1_000_000_000:
        score += 5

    score = max(0, min(100, score))

    return int(score)


def confidence_from_strength(score: int) -> str:

    if score >= 85:
        return "VERY HIGH"

    if score >= 70:
        return "HIGH"

    if score >= 55:
        return "MEDIUM"

    return "LOW"