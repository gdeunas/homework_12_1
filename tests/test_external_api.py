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


##


@patch("src.external_api.requests.request")
@patch("src.external_api.os.getenv")
@patch("src.external_api.load_dotenv")
def test_calc_amount_with_usd_eur_rub(mock_load_dotenv, mock_getenv, mock_request):
    transactions = [
        {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}},
        {"operationAmount": {"amount": "50", "currency": {"code": "EUR"}}},
        {"operationAmount": {"amount": "200", "currency": {"code": "RUB"}}},
    ]

    mock_getenv.return_value = "test_api_key"
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = {
        "rates": {"USD": "0.013", "EUR": "0.011"}
    }

    result = calc_amount(transactions)

    assert result == round(200 + 100 / 0.013 + 50 / 0.011, 2)
    mock_load_dotenv.assert_called_once()
    mock_getenv.assert_called_with("apikey")
    mock_request.assert_called_once()


@patch("src.external_api.requests.request")
@patch("src.external_api.os.getenv")
@patch("src.external_api.load_dotenv")
def test_calc_amount_no_transactions(mock_load_dotenv, mock_getenv, mock_request):
    result = calc_amount([])
    assert result == 0.0
    mock_load_dotenv.assert_not_called()
    mock_getenv.assert_not_called()
    mock_request.assert_not_called()
