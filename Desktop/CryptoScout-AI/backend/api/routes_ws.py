
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from core.ws_manager import manager
from core.redis_client import cache_get

router = APIRouter()


@router.websocket("/ws/signals")
async def websocket_signals(websocket: WebSocket):

    await manager.connect(websocket)

    # send cached signals
    recent = cache_get("recent_signals")

    if recent:
        await websocket.send_json({
            "type": "history",
            "data": recent
        })

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)