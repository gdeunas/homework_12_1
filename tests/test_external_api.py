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


@patch("src.external_api.convert_to_rub")
def test_calc_amount_with_mock_convert(mock_convert):
    mock_convert.side_effect = lambda amount, currency: (
        amount * 75 if currency == "USD" else amount * 85
    )

    transactions = [
        {"operationAmount": {"amount": "10", "currency": {"code": "USD"}}},
        {"operationAmount": {"amount": "20", "currency": {"code": "EUR"}}},
        {"operationAmount": {"amount": "1000", "currency": {"code": "RUB"}}},
    ]
    result = calc_amount(transactions)
    assert result == 3450.0


@patch("requests.get")
def test_convert_to_rub(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"conversion_rates": {"USD": 0.013, "EUR": 0.011}}
    mock_get.return_value = mock_response

    amount_usd = convert_to_rub(100, "USD")
    expected_usd = round(100 * round(1 / 0.013, 2), 2)
    assert amount_usd == expected_usd

    amount_eur = convert_to_rub(100, "EUR")
    expected_eur = round(100 * round(1 / 0.011, 2), 2)
    assert amount_eur == expected_eur

    api_token = "YOUR_API_TOKEN"
    # expected_url = f"https://v6.exchangerate-api.com/v6/{api_token}/latest/RUB"
    expected_url = "https://api.apilayer.com/exchangerates_data/convert"
    mock_get.assert_called()
