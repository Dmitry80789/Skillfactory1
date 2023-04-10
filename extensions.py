

import requests
import json
from config import keys

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            target_code  = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_code = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество валюты{amount}')

        if amount <= 0:
            raise APIException(f'Невозможно конверстировать количество валюты меньше или равное 0')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/6b814fb49ea3aa4dba843001/pair/{base_code}/{target_code}/{amount}')

        resp = json.loads(r.content)
        total_base = resp['conversion_rate'] * amount
        total_base = round(total_base, 3)
        total_base = f'Цена {amount} {base} в {quote} - {total_base}'



        return total_base