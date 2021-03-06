import uuid

import pytest  # type: ignore

from domains.users.repositories.user import UserRepository

repo = UserRepository()


@pytest.mark.asyncio
async def test_instantiate():
    assert repo


@pytest.mark.asyncio
async def test_get_by_id():
    result = await repo.get_by_id(uuid.uuid4())
    print(result)
