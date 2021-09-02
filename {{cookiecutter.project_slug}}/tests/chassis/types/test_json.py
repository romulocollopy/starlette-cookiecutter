from __future__ import annotations
import json
import datetime
from typing import Any

import pytest  # type: ignore

from chassis.types.json import JSON


DATE = datetime.date.today()
DATETIME = datetime.datetime.now()


@pytest.mark.parametrize(
    "input,parsed",
    [
        ({"spam": "eggs"}, {"spam": "eggs"}),
        (["spam", "eggs"], ["spam", "eggs"]),
        ('{"spam": "eggs"}', {"spam": "eggs"}),
        (b'{"spam": "eggs"}', {"spam": "eggs"}),
        (b'"spam"', "spam"),
        (
            [
                {"span": "eggs"},
                {"foo": "bar"},
                {"date": DATE},
                {"moment": DATETIME},
            ],
            [{"span": "eggs"}, {"foo": "bar"}, {"date": DATE}, {"moment": DATETIME}],
        ),
    ],
)
def test_parse_input(input: Any, parsed: Any) -> None:
    js = JSON(input)
    assert isinstance(js, JSON)
    assert js._data == parsed


def test_parse_date() -> None:
    data = json.dumps([
        {"date": DATE.isoformat()},
        {"moment": DATETIME.isoformat()},
    ])
    js = JSON(data)

    assert js._data == [{"date": DATE}, {"moment": DATETIME}]


def test_parse_date_on_key() -> None:
    data = json.dumps([
        {DATE.isoformat(): ["things"]},
        {DATETIME.isoformat(): {DATE.isoformat(): [DATETIME.isoformat()]}},
    ])
    js = JSON(data)

    assert js._data == [
        {DATE: ["things"]},
        {DATETIME: {DATE: [DATETIME]}},
    ]
