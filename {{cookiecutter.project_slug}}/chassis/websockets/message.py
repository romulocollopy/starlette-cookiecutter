from __future__ import annotations

from dataclasses import asdict, dataclass, field

from chassis.types.json import JSON


@dataclass
class Message:
    data: JSON
    type: str = "json"

    def to_json(self) -> JSON:
        return JSON(asdict(self))
