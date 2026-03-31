
# backend/api/routes_monitor.py

from fastapi import APIRouter
from datetime import datetime
import logging

from services.scanner_service import get_scan_status
from services.ai_service import ai_engine_health
from services.market_service import breaker
from services.market_service import api_tracker

from signals.signal_engine import generate_signals
from services.ranking_service import get_rankings
from core.redis_client import cache_get


router = APIRouter(prefix="/monitor")

logger = logging.getLogger(__name__)


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/")
def monitor():

    scan_info = get_scan_status()

    scanner = scan_info.get("scanner", {})

    overall_status = "healthy"

    if scanner.get("last_result") == "FAILED":
        overall_status = "degraded"

    if scanner.get("failure_count", 0) > 3:
        overall_status = "critical"

    api_snapshot = api_tracker.snapshot()

    if api_snapshot.get("calls_last_hour", 0) > 80:
        logger.warning("Approaching API budget limit")

    return {
        "overall_status": overall_status,
        "scanner": scanner,
        "api_failures": scan_info.get("api_failures", {}),
        "ai_engine": ai_engine_health(),
        "timestamp": datetime.utcnow().isoformat(),
        "market_circuit": breaker.snapshot(),
        "api_usage": api_snapshot
    }


@router.get("/signals")
async def get_signals():

    rankings = get_rankings(limit=200)

    signals = await generate_signals(rankings)

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

    #radar = []
    safe_signals = []

    for s in signals:
        if isisntance(s, dict):
            safe_signals.append(s)

    #for s in signals:
    #    if not isinstance(s, dict): #
    #        continue                #

        radar.append({
            "axis": s.get("type"),
            "symbol": s.get("symbol"),
            "value": s.get("strength", 0)
        })

    return radar


@router.get("/opportunity-heatmap")
def opportunity_heatmap():

    signals = cache_get("recent_signals") or []

    #heatmap = []

    safe_signals = []

    for s in signals:
        if isinstance(s,dict):
            safe_signals.append(s)

    #for s in signals:
    #    if not isinstance(s, dict): #
    #        continue                #

        heatmap.append({
            "symbol": s.get("symbol"),
            "market_cap": s.get("market_cap", 0),
            "momentum": s.get("change_24h", 0),
            "strength": s.get("strength", 0)
        })

    return heatmap


#@router.get("/")
#def monitor_root():
#    return {
#        "status": "monitor online",
#        "available_endpoints": [
#            "/monitor/opportunity-radar",
#            "/monitor/opportunity-heatmap"
#        ]
#    }

@router.get("/")
def monitor_root():
    try:
        signals = cache_get("recent_signals") or []

        return {
            "status": "monitor online",
            "signals_count": len(signals)
        }
    except Exception as e:
        return {"error": str(e)}