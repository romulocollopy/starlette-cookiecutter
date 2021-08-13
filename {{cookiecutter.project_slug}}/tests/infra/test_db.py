import pytest  # type: ignore

from infra.db import get_engine, init_db


def test_create_test_database():
    init_db()


@pytest.mark.asyncio
async def test_create_tables():
    await get_engine()
