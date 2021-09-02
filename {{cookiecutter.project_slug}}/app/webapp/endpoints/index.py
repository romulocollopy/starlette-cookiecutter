from __future__ import annotations

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse

from app import settings

PROJECT_NAME = "{{ cookiecutter.project_name }}"


class Index(HTTPEndpoint):
    async def get(self, request: Request) -> JSONResponse:
        return JSONResponse({"message": f"Welcome to {PROJECT_NAME}"})
