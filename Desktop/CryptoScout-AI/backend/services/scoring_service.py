# backend/services/scoring_service.py

import math
from typing import Dict, Any


# =====================================================
# SCORE CALCULATION
# =====================================================

def calculate_score(project: Dict[str, Any]) -> float:
    """
    Deterministic scoring engine used as fallback
    and baseline signal for CryptoScout.
    """

    market_cap = float(project.get("market_cap") or 0)
    volume = float(project.get("volume_24h") or 0)
    change_24h = float(project.get("price_change_24h") or 0)
    change_7d = float(project.get("price_change_7d") or 0)

    score = min(
        math.log10(market_cap + 1) * 15 +
        math.log10(volume + 1) * 12 +
        abs(change_24h) * 1.5 +
        abs(change_7d) * 0.8,
        100
    )

    return round(score, 2)


# =====================================================
# VERDICT GENERATION
# =====================================================

def verdict_from_score(score: float) -> str:
    """
    Translate score into investment signal.
    """

    if score >= 80:
        return "STRONG BUY"

    if score >= 65:
        return "BUY"

    if score >= 50:
        return "HOLD"

    return "AVOID"


# =====================================================
# FALLBACK ANALYSIS
# =====================================================

def fallback_analysis(project: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic fallback when AI is unavailable.
    """

    score = calculate_score(project)
    verdict = verdict_from_score(score)

    return {
        "score": score,
        "verdict": verdict,
        "confidence": round(score / 100, 2)
    }