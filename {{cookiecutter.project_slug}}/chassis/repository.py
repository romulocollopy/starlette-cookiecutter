from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Type
from uuid import UUID

from sqlalchemy import Table
from sqlalchemy.engine.cursor import CursorResult  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy.sql.selectable import Select

from chassis.exceptions import TableNotDefined
from chassis.models import BaseModel


@dataclass
class BaseRepository:
    session: ClassVar[AsyncSession | None] = None
    model: ClassVar[Type[BaseModel]] = BaseModel

    async def get_by_id(
        self, uuid: UUID | str, only_active: bool = True
    ) -> BaseModel | None:
        if only_active:
            qs = self.select_active()
        else:
            qs = self.select_all()

        result = await self.execute(qs.where(self.model.id == str(uuid)))
        return result.first()

    def select_active(self) -> Select:
        return self.select_all().where(self.model.active is True)

    def select_inactive(self) -> Select:
        return self.select_all().where(self.model.active == None)  # noqa: E711

    def select_all(self) -> Select:
        return self.table.select()

    @property
    def table(self) -> Table:
        if self.model.table is None:
            raise TableNotDefined(f"{self.model} didn't define a Table")
        return self.model.table

    @classmethod
    async def execute(cls, statement: ClauseElement) -> CursorResult:
        if not cls.session:
            await cls.connect()
            return await cls.execute(statement)

        async with cls.session() as session:
            async with session.begin():
                return await session.execute(statement)

    @classmethod
    async def connect(cls) -> None:
        from infra.db import get_engine

        if cls.session:
            return

        engine = await get_engine()
        cls.session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
