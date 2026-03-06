
# backend/signals/overheated.py

from typing import List, Dict


def detect_overheated(projects: List[Dict]) -> List[Dict]:

    alerts = []

    for p in projects:

        change = float(p.get("price_change_24h") or 0)

        if change > 25:

            alerts.append({
                "type": "OVERHEATED",
                "symbol": p.get("symbol"),
                "name": p.get("name"),
                "change_24h": change
            })

    return alerts