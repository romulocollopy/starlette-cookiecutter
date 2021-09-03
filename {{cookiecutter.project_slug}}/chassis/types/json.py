from __future__ import annotations

import copy
import datetime
import decimal
import json
import re
from dataclasses import dataclass, field
from typing import Any, Iterable, Union

JSONData = Union[dict, list, str, bytes, float, bool]
isoformatable = (datetime.datetime, datetime.date)


@dataclass
class JSON:
    _data: JSONData = field(default_factory=dict)
    _cached: None | str = None
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
        if self._cached is None:
            data = copy.deepcopy(self._data)
            self._cached = json.dumps(data, cls=CustomEncoder, sort_keys=True)
        return self._cached

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {str(self)}"

    def __getattr__(self, name: str) -> Any:
        return JSON(self._data[name])

    def __getitem__(self, index: int) -> Any:
        return JSON(self._data[index])

    @property
    def data(self) -> JSONData:
        return self._data

    @data.setter
    def set_data(self, value):
        self._cached = None
        self._data = value


class CustomEncoder(json.JSONEncoder):
    @staticmethod
    def _is_valid_key(obj: Any) -> bool:
        valid_types = (str, int, float, bool)
        if isinstance(obj, valid_types) or obj is None:
            return True

        return False

    def encode(self, obj: Any) -> Any:
        if self._is_valid_key(obj):
            return super().encode(obj)

        self.walk(obj)
        return super().encode(obj)

    def walk(self, obj: Iterable) -> Any:
        if self._is_valid_key(obj):
            return obj

        if isinstance(obj, isoformatable):
            return obj.isoformat()

        if isinstance(obj, dict):
            keys = tuple(obj.keys())
            for k in keys:
                v = obj[k]
                if isinstance(k, isoformatable):
                    _k = k.isoformat()
                    obj[_k] = self.walk(v)
                    del obj[k]

                elif isinstance(k, decimal.Decimal):
                    _k = str(k)
                    obj[_k] = self.walk(v)
                    del obj[k]

                else:
                    obj[k] = self.walk(v)

        if isinstance(obj, list):
            for i in range(len(obj)):
                obj[i] = self.walk(obj[i])

        return obj


class CustomDecoder(json.JSONDecoder):
    is_date = re.compile(r"\d{4}-\d{2}-\d{2}")
    is_datetime = re.compile(r"\d{4}-\d{2}-\d{2}T.*")

    def __init__(self, parse_dates: bool = False, *args: Any, **kwargs: Any) -> None:
        super().__init__(object_hook=self._parse_string, *args, **kwargs)
        self.parse_dates = parse_dates

    def _parse_string(self, obj: dict) -> dict:
        if not self.parse_dates:
            return obj
        print(obj)
        return self.walk(obj)

    @classmethod
    def _parse_dates(cls, data: str) -> datetime.datetime | datetime.date:
        if cls.is_datetime.match(data):
            return datetime.datetime.fromisoformat(data)

        if cls.is_date.match(data):
            return datetime.date.fromisoformat(data)

        raise ValueError

    def walk(self, obj: Iterable) -> Any:
        if isinstance(obj, str):
            try:
                return self._parse_dates(obj)
            except (ValueError, TypeError):
                return obj

        if isinstance(obj, dict):
            keys = tuple(obj.keys())
            for k in keys:
                v = obj[k]
                try:
                    _k = self._parse_dates(k)
                except (ValueError, TypeError):
                    if isinstance(v, dict):
                        continue
                    obj[k] = self.walk(v)
                else:
                    del obj[k]
                    if isinstance(v, dict):
                        obj[_k] = v
                    else:
                        obj[_k] = self.walk(v)

        if isinstance(obj, list):
            for i in range(len(obj)):
                li = obj[i]
                if isinstance(li, str):
                    try:
                        obj[i] = self._parse_dates(li)
                    except ValueError:
                        pass
                self.walk(li)

        return obj
