
# backend/scheduler.py

import threading
import time
import logging
import asyncio

from services.scanner_service import run_scan_sync
from services.ranking_service import get_rankings
from signals.signal_engine import generate_signals
from core.ws_manager import manager
from core.redis_client import cache_set
from services.market_narrative_service import generate_market_narrative
from services.ai_service import pre_analyze_projects


logger = logging.getLogger(__name__)

# =====================================================
# CONFIG
# =====================================================

SCAN_INTERVAL_SECONDS = 300  # 5 minutes

_scheduler_thread = None
_running = False
_lock = threading.Lock()


# =====================================================
# SAFE SCAN WRAPPER
# =====================================================

def _safe_scan():
    """
    Ensures only one scan runs at a time.
    """

    if not _lock.acquire(blocking=False):
        logger.warning("Scan skipped — previous scan still running")
        return

    try:

        # 1️⃣ Run market scan
        run_scan_sync()

        # 2️⃣ Get ranked projects
        projects = get_rankings(limit=200)

        # AI pre-analysis for top coins
        pre_analyze_projects(projects, limit=100)

        # 3️⃣ Generate signals
        signals = generate_signals(projects)

        # 4️⃣ Cache signals in Redis
        cache_set("recent_signals", signals, 300)

        # NEW: generate market narrative
        generate_market_narrative(projects, signals)

        # 5️⃣ Broadcast signals
        if signals:
            asyncio.run(_broadcast_signals(signals))

    finally:
        _lock.release()


# =====================================================
# BROADCAST SIGNALS
# =====================================================

async def _broadcast_signals(signals):

    for signal in signals:

        await manager.broadcast({
            "type": "signal",
            "data": signal
        })


# =====================================================
# BACKGROUND LOOP
# =====================================================

def _scheduler_loop():
    global _running

    logger.info("Scheduler started (interval: %s sec)", SCAN_INTERVAL_SECONDS)

    while _running:

        try:
            _safe_scan()

        except Exception as e:
            logger.error("Scheduler error: %s", e)

        time.sleep(SCAN_INTERVAL_SECONDS)

    logger.info("Scheduler stopped")


# =====================================================
# PUBLIC CONTROL
# =====================================================

def start_scheduler():
    global _scheduler_thread, _running

    if _scheduler_thread and _scheduler_thread.is_alive():
        logger.warning("Scheduler already running")
        return

    _running = True

    _scheduler_thread = threading.Thread(
        target=_scheduler_loop,
        daemon=True
    )

    _scheduler_thread.start()


def stop_scheduler():
    global _running
    _running = False