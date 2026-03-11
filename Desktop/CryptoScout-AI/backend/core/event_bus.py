
import asyncio
import logging

from core.ws_manager import manager

logger = logging.getLogger(__name__)


async def emit(event: str, data: dict):
    """
    Emit an event to all WebSocket clients.
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
    Safe sync wrapper (for scheduler threads)
    """

    try:
        loop = asyncio.get_event_loop()

        if loop.is_running():
            asyncio.create_task(emit(event, data))
        else:
            asyncio.run(emit(event, data))

    except RuntimeError:
        asyncio.run(emit(event, data))