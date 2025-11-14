from unittest.mock import MagicMock, patch

import pytest

from src.external_api import calc_amount, convert_to_rub


@pytest.mark.parametrize(
    "transactions, expected",
    [
        (
            [
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
                }
            ],
            31957.58,
        ),
        ([], 0.0),
        (None, 0.0),
        ([{"some_key": {}}], 0.0),
    ],
)
def test_calc_amount(transactions, expected):
    assert calc_amount(transactions) == expected


transactions_sample = [
    {"operationAmount": {"amount": "100", "currency": {"code": "RUB"}}},
    {"operationAmount": {"amount": "10", "currency": {"code": "USD"}}},
    {"operationAmount": {"amount": "20", "currency": {"code": "EUR"}}},
]


@patch("src.external_api.requests.request")
@patch("src.external_api.os.getenv")
def test_calc_amount_total(mock_getenv, mock_request):
    mock_getenv.return_value = "fake_api_key"
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"USD": 0.013, "EUR": 0.011}}
    mock_request.return_value = mock_response

    total = calc_amount(transactions_sample)
    expected = 100 + 10 / 0.013 + 20 / 0.011
    assert abs(total - expected) < 0.01


def test_calc_amount_empty_list():
    assert calc_amount([]) == 0.0


def test_calc_amount_none():
    assert calc_amount(None) == 0.0


@patch("src.external_api.requests.request")
@patch("src.external_api.os.getenv")
def test_convert_to_rub_correct_conversion(mock_getenv, mock_request):
    mock_getenv.return_value = "fake_api_key"
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"USD": 0.013, "EUR": 0.011}}
    mock_request.return_value = mock_response

    result = convert_to_rub(transactions_sample)
    expected = 10 / 0.013 + 20 / 0.011
    assert abs(result - expected) < 0.01
