
from fastapi import APIRouter
from core.redis_client import cache_get

router = APIRouter(prefix="/signals", tags=["Signals"])

@router.get("/")
def get_signals():
    return cache_get("recent_signals") or []