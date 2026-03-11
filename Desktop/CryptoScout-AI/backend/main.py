
# backend/main.py

import os
import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from core.config import APP_NAME, ALLOWED_ORIGINS
from core.logging_config import setup_logging
from database.db import init_db, run_migrations
from scheduler import start_scheduler

from api.routes_auth import router as auth_router
from api.routes_rankings import router as rankings_router
from api.routes_watchlist import router as watchlist_router
from api.routes_monitor import router as monitor_router
from api.routes_backtest import router as backtest_router
from api.routes_alerts import router as alerts_router
from api.routes_ws import router as ws_router
from api.routes_ai import router as ai_router
from services.payments_service import router as payments_router
from api.routes_signals import router as signals_router


# =====================================================
# LOGGING FIRST
# =====================================================

setup_logging()


# =====================================================
# CREATE APP (MUST COME EARLY)
# =====================================================

app = FastAPI(title=APP_NAME)


# =====================================================
# SECURITY HEADERS
# =====================================================

@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
    return response


# =====================================================
# CORS MIDDLEWARE
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# OPTIONAL GZIP
# =====================================================

app.add_middleware(GZipMiddleware, minimum_size=500)


# =====================================================
# SENTRY
# =====================================================

SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=1.0
    )


# =====================================================
# STARTUP EVENT
# =====================================================

@app.on_event("startup")
async def startup_event():
    # Initialize DB and run migrations
    init_db()
    run_migrations()
    # Start background scheduler
    start_scheduler()


@app.on_event("startup")
def startup_event():
    init_db()
    run_migrations()
    start_scheduler()

    print("🚀 Backend started")
    print("📡 WebSocket system ready")

# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
async def health():
    return {"status": "ok"}


# =====================================================
# ROUTERS
# =====================================================

app.include_router(auth_router)
app.include_router(rankings_router)
app.include_router(watchlist_router)
app.include_router(monitor_router)
app.include_router(backtest_router)
app.include_router(alerts_router)
app.include_router(ws_router)
app.include_router(ai_router, prefix="/ai")
app.include_router(payments_router)
app.include_router(signals_router)