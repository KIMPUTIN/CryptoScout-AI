
# backend/signals/signal_engine.py

from typing import List, Dict, Any

from signals.breakout import detect_breakouts
from signals.gem_detector import detect_hidden_gems
from signals.overheated import detect_overheated
from signals.scoring import compute_signal_strength, confidence_from_strength
from signals.alpha_finder import detect_alpha
from signals.momentum_acceleration import detect_momentum_acceleration


def generate_signals(projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

    signals: List[Dict[str, Any]] = []

    detectors = [
        detect_breakouts,
        detect_hidden_gems,
        detect_overheated,
        detect_alpha,
        detect_momentum_acceleration,
    ]

    for detector in detectors:
        results = detector(projects)

        if results:
            signals.extend(results)

    # 🔥 NEW: build lookup for project data
    project_lookup = {
        p.get("symbol"): p for p in projects
    }

    for signal in signals:

        if not isinstance(signal, dict):
            continue

        symbol = signal.get("symbol")
        project = project_lookup.get(symbol, {})

        # 🔥 ENRICH SIGNAL WITH MARKET DATA
        signal["market_cap"] = project.get("market_cap", 0)
        signal["volume_24h"] = project.get("volume_24h", 0)
        signal["price_change_24h"] = project.get("price_change_24h", 0)
        signal["ai_score"] = project.get("ai_score", 0)


        strength = compute_signal_strength(signal)

        signal["strength"] = strength
        signal["confidence"] = confidence_from_strength(strength)

    signals.sort(key=lambda x: x.get("strength", 0), reverse=True)

    return signals