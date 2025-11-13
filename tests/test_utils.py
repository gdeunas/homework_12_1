from unittest.mock import patch

import pytest

from src.utils import json_filter


@pytest.mark.parametrize(
    "path, expected",
    [
        ("", []),
    ],
)
def test_json_filter_empty_path(path, expected):
    assert json_filter(path) == expected


@patch("builtins.open")
@patch("json.load")
def test_json_filter_path(mock_json_load, mock_file):
    mock_json_load.return_value = [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        },
    ]
    result = json_filter("data/operations.json")
    mock_file.assert_called_once_with("data/operations.json", encoding="utf-8")
    mock_json_load.assert_called_once()
    assert result == mock_json_load.return_value
