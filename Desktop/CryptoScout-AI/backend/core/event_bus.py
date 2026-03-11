
import asyncio
import logging

from core.ws_manager import manager

logger = logging.getLogger(__name__)

# reference to the main FastAPI loop
_main_loop = None


def set_event_loop(loop):
    """
    Called during FastAPI startup to store the main loop.
    """
    global _main_loop
    _main_loop = loop


async def emit(event: str, data: dict):
    """
    Emit an event to WebSocket clients.
    """

    message = {
        "event": event,
        "data": data
    }

    try:
        await manager.broadcast(message)

    except Exception as e:
        logger.error("Event broadcast failed: %s", e)


def emit_sync(event: str, data: dict):
    """
    Thread-safe emitter for scheduler/background threads.
    """

    if _main_loop is None:
        logger.error("Event loop not initialized for event bus")
        return

    asyncio.run_coroutine_threadsafe(
        emit(event, data),
        _main_loop
    )