from __future__ import annotations

from starlette.routing import Route, WebSocketRoute

from .endpoints import WebSocketHandler
# from .endpoints import Index
from .endpoints.home import Home

ROUTES: list[Route] = [
    # Route("/", endpoint=Index),
    Route("/", endpoint=Home),
    WebSocketRoute("/ws", WebSocketHandler)
]
