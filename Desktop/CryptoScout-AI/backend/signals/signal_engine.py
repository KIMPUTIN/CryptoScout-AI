
# backend/signals/signal_engine.py

from typing import List, Dict

from signals.breakout import detect_breakouts
from signals.gem_detector import detect_hidden_gems
from signals.overheated import detect_overheated

from signals.scoring import compute_signal_strength, confidence_from_strength
from signals.alpha_finder import detect_alpha
from signals.momentum_acceleration import detect_momentum_acceleration

def generate_signals(projects):

    signals = []

    signals += detect_breakouts(projects)
    signals += detect_hidden_gems(projects)
    signals += detect_overheated(projects)
    signals += detect_alpha(projects)
    signals += detect_momentum_acceleration(projects)

    for signal in signals:

        strength = compute_signal_strength(signal)

        signal["strength"] = strength
        signal["confidence"] = confidence_from_strength(strength)

    signals.sort(key=lambda x: x.get("strength", 0), reverse=True)

    return signals