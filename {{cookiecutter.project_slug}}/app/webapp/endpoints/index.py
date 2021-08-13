from __future__ import annotations

from app import settings
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse


class Index(HTTPEndpoint):
    async def get(self, request: Request) -> JSONResponse:
        return JSONResponse({"database": str(settings.DATABASE_URL)})
