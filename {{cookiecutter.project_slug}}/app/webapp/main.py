from __future__ import annotations

from starlette.applications import Starlette

from app import settings
from chassis.repository import BaseRepository

from .routes import ROUTES

app = Starlette(
    debug=settings.DEBUG, routes=ROUTES, on_startup=[BaseRepository.connect]
)
