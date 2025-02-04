from fastapi import WebSocket, status, Query
from typing import Optional


Redis = None

async def get_token(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
):
    from ..redis.config import Redis
    global Redis
    redis = Redis()

    if token is None or token == "":
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    redis_client = await redis.create_connection()
    isexists = await redis_client.exists(token)

    if isexists == 1:
        return token
    else:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Session not authenticated or expired token")
