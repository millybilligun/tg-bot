import requests
import json

class APIException(Exception):
    """Класс для пользовательских исключений."""
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        """Метод для получения курса валют."""
        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Количество должно быть числом.")
        
        if base == quote:
            raise APIException("Невозможно перевести одинаковые валюты.")
        
        # Пример API для курсов валют (замените на удобный API, если нужно)
        url = f"https://api.exchangerate-api.com/v4/latest/{base.upper()}"

        try:
            response = requests.get(url)
            data = json.loads(response.text)
        except Exception as e:
            raise APIException(f"Ошибка получения данных от API: {e}")

        if quote.upper() not in data['rates']:
            raise APIException(f"Валюта {quote} недоступна для конвертации.")
        
        rate = data['rates'][quote.upper()]
        total = rate * amount
        return round(total, 2)