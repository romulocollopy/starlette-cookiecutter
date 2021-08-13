from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from itertools import chain
from uuid import UUID

import sqlalchemy  # type: ignore
from sqlalchemy.dialects.postgresql import UUID as UUIDField  # type: ignore
from sqlalchemy.orm import registry  # type: ignore

mapper_registry = registry()
metadata = sqlalchemy.MetaData()


DEFAULT_INDEX = sqlalchemy.Index("id_active", "id", "active")
DEFAULT_COLUMS = (
    sqlalchemy.Column("id", UUIDField, primary_key=True),
    sqlalchemy.Column("active", sqlalchemy.Boolean, nullable=True),
    sqlalchemy.Column(
        "created_at",
        sqlalchemy.DateTime,
        nullable=False,
        server_default=sqlalchemy.sql.func.now(),
    ),
    sqlalchemy.Column(
        "updated_at",
        sqlalchemy.DateTime,
        nullable=False,
        server_onupdate=sqlalchemy.sql.func.now(),
    ),
)


@dataclass
class BaseModel:
    table: sqlalchemy.Table | None
    id: UUID = field(init=False)
    active: None | bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def deactivate(self) -> None:
        self.updated_at = datetime.now()
        self.active = None

    def activate(self) -> None:
        self.updated_at = datetime.now()
        self.active = True

    @classmethod
    def register(cls, table: sqlalchemy.Table, **properties) -> None:
        cls.table = table
        mapper_registry.map_imperatively(cls, table, properties=properties)

    @classmethod
    def build_table(cls, *args, **kwargs) -> sqlalchemy.Table:
        args = tuple(a for a in chain(args, DEFAULT_COLUMS, [DEFAULT_INDEX]))
        table_name = kwargs.pop("table_name", None) or f"{cls.__name__.lower()}s"
        kwargs["schema"] = kwargs.get("schema", "public")
        return sqlalchemy.Table(table_name, metadata, *args, **kwargs)
