from __future__ import annotations

import asyncio

from alembic import command  # type: ignore
from alembic.config import Config  # type: ignore
from asyncpg.exceptions import InvalidCatalogNameError  # type: ignore
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine  # type: ignore
from sqlalchemy.ext.asyncio.engine import AsyncEngine  # type: ignore

from app import settings
from chassis.models import metadata


def run_migrations() -> None:
    script_location = "migrations"
    dsn = str(settings.DATABASE_URL)
    alembic_cfg = Config(str(settings.BASE_DIR / "alembic.ini"))
    alembic_cfg.set_main_option("script_location", script_location)
    alembic_cfg.set_main_option("sqlalchemy.url", dsn)
    command.upgrade(alembic_cfg, "head")


def init_db() -> None:
    asyncio.run(setup_db())


async def get_engine() -> AsyncEngine:
    return create_async_engine(str(settings.DATABASE_URL), echo=settings.DEBUG)


async def setup_db() -> None:
    engine = create_async_engine(str(settings.DATABASE_URL), echo=settings.DEBUG)
    try:
        async with engine.connect() as conn:
            await conn.run_sync(metadata.create_all)
    except InvalidCatalogNameError:
        await create_db()
        await setup_db()


async def create_db() -> None:
    database_url = settings.DATABASE_URL
    db_name = database_url.path[1:]
    db_server = str(database_url.replace(path=""))
    engine = create_async_engine(db_server, isolation_level="AUTOCOMMIT")
    async with engine.connect() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS public;"))
        await conn.execute(text(f"CREATE DATABASE {db_name};"))


def teardown_db() -> None:
    asyncio.run(drop_test_db())


async def drop_test_db() -> None:
    if "test" not in settings.DATABASE_URL.path:
        return

    engine = create_async_engine(
        str(settings.DATABASE_URL), isolation_level="AUTOCOMMIT"
    )

    async with engine.connect() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.execute(text("DROP table alembic_version;"))
