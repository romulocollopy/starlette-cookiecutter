from __future__ import annotations

from starlette.routing import Route
from .endpoints import Index

ROUTES: list[Route] = [
    Route("/", endpoint=Index),
]
