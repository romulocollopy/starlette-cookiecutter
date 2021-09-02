from __future__ import annotations
import re
import datetime
import decimal
import json
from dataclasses import dataclass, field
from typing import Any, Union, Iterable

JSONData = Union[dict, list, str, bytes]


@dataclass
class JSON:
    _data: JSONData = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not (isinstance(self._data, dict) or isinstance(self._data, list)):
            self._data = json.loads(
                self._data,
                parse_float=decimal.Decimal,
                cls=CustomDecoder,
            )

    def __str__(self) -> str:
        return json.dumps(self._data, cls=CustomEncoder, sort_keys=True)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {str(self)}"

    def __getattr__(self, name: str | int) -> Any:
        if not isinstance(self._data, dict):
            return self._data[int(name)]

        return self._data[name]


class CustomEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime.date) or isinstance(obj, datetime.datetime):
            return obj.isoformat()

        if isinstance(obj, decimal.Decimal):
            return str(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class CustomDecoder(json.JSONDecoder):
    def decode(self, obj: str) -> JSONData:
        obj = super().decode(obj)
        return self.walk(obj)

    def walk(self, obj: Iterable) -> Any:
        if isinstance(obj, str):
            try:
                return parse_dates(obj)
            except ValueError:
                return obj

        if isinstance(obj, dict):
            keys = tuple(obj.keys())
            for k in keys:
                try:
                    _k = parse_dates(k)
                except ValueError:
                    obj[k] = self.walk(obj[k])
                else:
                    obj[_k] = self.walk(obj[k])
                    del obj[k]

        if isinstance(obj, list):
            for i in range(len(obj)):
                if isinstance(obj[i], str):
                    try:
                        obj[i] = parse_dates(obj[i])
                    except ValueError:
                        pass
                self.walk(obj[i])

        return obj


def parse_dates(data: str) -> datetime.datetime | datetime.date:
    is_date = re.compile(r"\d{4}-\d{2}-\d{2}")
    is_datetime = re.compile(r"\d{4}-\d{2}-\d{2}T.*")

    if is_datetime.match(data):
        return datetime.datetime.fromisoformat(data)

    if is_date.match(data):
        return datetime.date.fromisoformat(data)

    raise ValueError
