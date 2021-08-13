from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import Column, String

from chassis.models import BaseModel


@dataclass
class User(BaseModel):
    name: str | None = None
    fullname: str | None = None
    nickname: str | None = None


User.register(
    User.build_table(
        Column("name", String(50)),
        Column("fullname", String(50)),
        Column("nickname", String(12)),
    ),
)
