# import os
import json

# from external_api import calc_amount


def json_filter(path_to: str) -> list[dict]:
    """Реализуйте функцию, которая принимает на вход путь до JSON-файла и возвращает список словарей с
    данными о финансовых транзакциях. Если файл пустой, содержит не список или не найден, функция возвращает
    пустой список. Функцию поместите в модуль utils. Файл с данными о финансовых транзациях operations.json
    поместите в директорию data/ в корне проекта."""
    if path_to:
        with open(path_to, encoding="utf-8") as f:
            data = json.load(f)
        return data
    else:
        return []


# call funcs
# path = os.path.join(
#     os.path.dirname(os.path.dirname(__file__)), "data", "operations.json"
# )
# # print(json_filter(path))
#
# print(calc_amount(json_filter(path)))
