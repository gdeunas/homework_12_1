import os
from json import JSONDecodeError
from typing import Union

import requests
from dotenv import load_dotenv


def calc_amount(transactions: Union[list[dict] | None]) -> float:
    """Calculate total amount in RUB from transactions, converting USD and EUR."""
    s_amount = 0.0
    try:
        if transactions:
            s_amount += convert_to_rub(transactions)
            s_amount += sum(
                float(t["operationAmount"]["amount"])
                for t in transactions
                if t["operationAmount"]["currency"]["code"] == "RUB"
            )
    except (KeyError, TypeError):
        pass
    return round(s_amount, 2)


def convert_to_rub(transactions: list[dict]) -> float:
    """Convert USD and EUR amounts in transactions to RUB."""
    s_amount = 0.0
    try:
        load_dotenv()
        # api_token = os.getenv("EXCHANGE_RATE_API_KEY")
        api_token = os.getenv("apikey")
        if not api_token:
            print("API token missing")
            return 0.0

        # url = f"https://v6.exchangerate-api.com/v6/{api_token}/latest/RUB"
        url = "https://api.apilayer.com/exchangerates_data/latest?symbols=USD%2C%20EUR&base=RUB"
        headers = {"apikey": api_token}
        response = requests.request("GET", url, headers=headers)

        if response.status_code != 200:
            print(response.status_code)
            raise ValueError("Failed to get currency rate")

        # response.raise_for_status()
        data = response.json()
        currency_data_usd = data["rates"].get("USD")
        if not currency_data_usd:
            raise ValueError("No data for currency USD")

        currency_data_eur = data["rates"].get("EUR")
        if not currency_data_eur:
            raise ValueError("No data for currency EUR")

        # usd_to_rub = round(1 / data["conversion_rates"]["USD"], 2)
        # eur_to_rub = round(1 / data["conversion_rates"]["EUR"], 2)
        usd_to_rub = 1 / float(currency_data_usd)
        eur_to_rub = 1 / float(currency_data_eur)

        s_amount_usd = 0.0
        s_amount_eur = 0.0
        for t in transactions:
            op_amount = t.get("operationAmount")
            # print(op_amount)
            if op_amount and "amount" in op_amount and "currency" in op_amount:
                currency = op_amount["currency"]
                if currency and "code" in currency:
                    if currency["code"] == "USD":
                        s_amount_usd += float(op_amount["amount"])
                    if currency["code"] == "EUR":
                        s_amount_eur += float(op_amount["amount"])

        s_amount = s_amount_usd * usd_to_rub
        s_amount += s_amount_eur * eur_to_rub

    except (KeyError, requests.RequestException, ValueError) as e:
        print(f"Error during conversion: {e}")
        pass
    except FileNotFoundError:
        print("File .env not found. Check the path.")
    except JSONDecodeError:
        print("JSONDecodeError JSON from requests.")

    return s_amount
