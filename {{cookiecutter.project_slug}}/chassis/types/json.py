from __future__ import annotations

import datetime
import decimal
import json
import re
from dataclasses import dataclass, field
from typing import Any, Iterable, Union

JSONData = Union[dict, list, str, bytes]


@dataclass
class JSON:
    _data: JSONData = field(default_factory=dict)
    parse_dates: bool = False

    def __post_init__(self) -> None:
        if not (isinstance(self._data, dict) or isinstance(self._data, list)):
            self._data = json.loads(
                self._data,
                parse_float=decimal.Decimal,
                parse_dates=self.parse_dates,
                cls=CustomDecoder,
            )

    def __str__(self) -> str:
        return json.dumps(self._data, cls=CustomEncoder, sort_keys=True)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {str(self)}"

    def __getattr__(self, name: str | int) -> Any:
        if not isinstance(self._data, dict):
            return self._data[int(name)]

        return JSON(self._data[name])


class CustomEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime.date) or isinstance(obj, datetime.datetime):
            return obj.isoformat()

        if isinstance(obj, decimal.Decimal):
            return str(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class CustomDecoder(json.JSONDecoder):
    is_date = re.compile(r"\d{4}-\d{2}-\d{2}")
    is_datetime = re.compile(r"\d{4}-\d{2}-\d{2}T.*")

    def __init__(self, parse_dates: bool = False, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.parse_dates = parse_dates

    def decode(self, obj: str) -> JSONData:
        obj = super().decode(obj)
        if not self.parse_dates:
            return obj
        return self.walk(obj)

    def _parse_dates(self, data: str) -> datetime.datetime | datetime.date:
        if self.is_datetime.match(data):
            return datetime.datetime.fromisoformat(data)

        if self.is_date.match(data):
            return datetime.date.fromisoformat(data)

        raise ValueError

    def walk(self, obj: Iterable) -> Any:
        if isinstance(obj, str):
            try:
                return self._parse_dates(obj)
            except ValueError:
                return obj

        if isinstance(obj, dict):
            keys = tuple(obj.keys())
            for k in keys:
                try:
                    _k = self._parse_dates(k)
                except ValueError:
                    obj[k] = self.walk(obj[k])
                else:
                    obj[_k] = self.walk(obj[k])
                    del obj[k]

        if isinstance(obj, list):
            for i in range(len(obj)):
                if isinstance(obj[i], str):
                    try:
                        obj[i] = self._parse_dates(obj[i])
                    except ValueError:
                        pass
                self.walk(obj[i])

        return obj
