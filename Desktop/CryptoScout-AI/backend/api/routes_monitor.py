
# backend/api/routes_monitor.py

from fastapi import APIRouter
from datetime import datetime

from services.scanner_service import get_scan_status
from services.ai_service import ai_engine_health
from services.market_service import breaker
from services.market_service import api_tracker

from signals.signal_engine import generate_signals
from services.ranking_service import get_rankings
from core.redis_client import cache_get



router = APIRouter(prefix="/monitor")


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/monitor")
def monitor():

    scan_info = get_scan_status()

    overall_status = "healthy"

    if scan_info["scanner"]["last_result"] == "FAILED":
        overall_status = "degraded"

    if scan_info["scanner"]["failure_count"] > 3:
        overall_status = "critical"

    if api_tracker.snapshot()["calls_last_hour"] > 80:
        logger.warning("Approaching API budget limit")


    return {
        "overall_status": overall_status,
        "scanner": scan_info["scanner"],
        "api_failures": scan_info["api_failures"],
        "ai_engine": ai_engine_health(),
        "timestamp": datetime.utcnow().isoformat(),
        "market_circuit": breaker.snapshot(),
        "api_usage": api_tracker.snapshot()
    }

@router.get("/signals")
def get_signals():

    rankings = get_rankings(limit=200)

    signals = generate_signals(rankings)

    return signals


@router.get("/market-narrative")
def market_narrative():

    narrative = cache_get("market_narrative")

    return {
        "narrative": narrative
    }


@router.get("/opportunity-radar")
def opportunity_radar():

    signals = cache_get("recent_signals") or []

    radar = []

    for s in signals:

        radar.append({
            "axis": s.get("type"),
            "symbol": s.get("symbol"),
            "value": s.get("strength", 0)
        })

    return radar


@router.get("/opportunity-heatmap")
def opportunity_heatmap():

    signals = cache_get("recent_signals") or []

    heatmap = []

    for s in signals:

        heatmap.append({
            "symbol": s.get("symbol"),
            "market_cap": s.get("market_cap", 0),
            "momentum": s.get("change_24h", 0),
            "strength": s.get("strength", 0)
        })

    return heatmap