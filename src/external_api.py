import os

import requests
from dotenv import load_dotenv


def calc_amount(transactions) -> float:
    """Реализуйте функцию, которая принимает на вход транзакцию и возвращает сумму транзакции (
    amount) в рублях, тип данных — float. Если транзакция была в USD или EUR,
    происходит обращение к внешнему API для получения текущего курса валют и конвертации суммы операции в рубли.
    Для конвертации валюты воспользуйтесь Exchange Rates Data API: https://apilayer.com/exchangerates_data-api.
    Функцию конвертации поместите в модуль external_api"""
    s_amount = 0.0
    try:
        if transactions:
            for transaction in transactions:
                if transaction["operationAmount"]["currency"]["code"] == "USD":
                    s_amount += convert_to_rub(
                        float(transaction["operationAmount"]["amount"]), "USD"
                    )
                elif transaction["operationAmount"]["currency"]["code"] == "EUR":
                    s_amount += convert_to_rub(
                        float(transaction["operationAmount"]["amount"]), "EUR"
                    )
                elif transaction["operationAmount"]["currency"]["code"] == "RUB":
                    s_amount += float(transaction["operationAmount"]["amount"])
    except KeyError:
        # действия если ключа нет
        pass
    return round(float(s_amount), 2)


def convert_to_rub(amount, currency: str) -> float:
    """конвертация суммы операции в рубли"""
    try:
        load_dotenv()
        api_token = os.getenv("exchangerate-api")

        # url = "https://api.apilayer.com/exchangerates_data/convert"

        # headers = {
        #     "apikey": "WkzH6EmMSSbRCQkuUkGoT2E1n6K5wTKi"
        # }

        url = f"https://v6.exchangerate-api.com/v6/{api_token}/latest/RUB"
        headers = {"apikey": f"{api_token}"}

        response = requests.get(url, headers=headers)
        repos = response.json()

        # status_code = response.status_code
        usb_rub = round(1 / repos["conversion_rates"]["USD"], 2)
        eur_rub = round(1 / repos["conversion_rates"]["EUR"], 2)
        if currency == "USD":
            return amount * usb_rub
        elif currency == "EUR":
            return amount * eur_rub
    except KeyError:
        # действия если ключа нет
        pass
    return 0.0
