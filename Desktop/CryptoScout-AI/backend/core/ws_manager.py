
# backend/core/ws_manager.py

import asyncio
import logging
from typing import List

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:

    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        async with self.lock:
            self.active_connections.append(websocket)
        logger.info("WebSocket connected. Total connections: %d", len(self.active_connections))

    async def disconnect(self, websocket: WebSocket):
        async with self.lock:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
        logger.info("WebSocket disconnected. Total connections: %d", len(self.active_connections))

    async def broadcast(self, message: dict) -> None:
        """
        Send a message to all connected clients.
        """
        async with self.lock:
            connections = list(self.active_connections)

        for connection in connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.warning("Failed to send message to client: %s", e)


# Singleton instance
manager = ConnectionManager()