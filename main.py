import os

from src.external_api import calc_amount
from src.utils import json_filter

# call funcs
path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "homework_12_1/data", "operations.json"
)
# # print(json_filter(path))
#
print(calc_amount(json_filter(path)))


# url = "https://api.apilayer.com/exchangerates_data/convert?to=to&from=from&amount=amount"
# response usd
# {
#   "date": "2025-11-14",
#   "info": {
#     "rate": 80.977404,
#     "timestamp": 1763114643
#   },
#   "query": {
#     "amount": 1,
#     "from": "USD",
#     "to": "RUB"
#   },
#   "result": 80.977404,
#   "success": true
# }


# url = "https://api.apilayer.com/exchangerates_data/latest?symbols=USD%2C%20EUR&base=RUB"
# response usd eur
# {
#   "base": "RUB",
#   "date": "2025-11-14",
#   "rates": {
#     "EUR": 0.010627,
#     "USD": 0.012348
#   },
#   "success": true,
#   "timestamp": 1763114944
# }

#
# return
# 80.99789405475458
# 94.09993413004611
# 190093160.54
