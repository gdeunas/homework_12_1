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


@patch('json.load')
@patch('builtins.open')
def test_json_filter_(mock_open, mock_load):
    """Тест: функция json_filter с декоратором patch."""
    mock_open.return_value.__enter__.return_value = 'dummy file'
    mock_load.return_value = [{"id": 1, "amount": 100}]

    result = json_filter("dummy_path.json")
    assert result == [{"id": 1, "amount": 100}]
    mock_open.assert_called_once_with("dummy_path.json", encoding="utf-8")
    mock_load.assert_called_once()


@patch('builtins.open', side_effect=FileNotFoundError)
def test_json_filter_file_not_found(mock_open):
    result = json_filter("nonexistent.json")
    assert result == []
