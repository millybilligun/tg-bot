# main.py
import telebot
from config import TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    """Отправляет инструкции пользователю."""
    text = (
        "Чтобы узнать цену валюты, отправьте сообщение в формате:\n"
        "<имя валюты> <имя валюты для конвертации> <количество>\n"
        "Пример: евро доллар 100\n"
        "Доступные команды:\n"
        "/start или /help — инструкции по использованию\n"
        "/values — список доступных валют"
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def list_values(message):
    """Выводит список доступных валют."""
    text = "Доступные валюты: евро, доллар, рубль"
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert_currency(message):
    """Обрабатывает запрос пользователя для конвертации валют."""
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException("Неправильный формат запроса. Используйте формат: <валюта> <валюта для конвертации> <количество>")
        
        base, quote, amount = values
        total = CurrencyConverter.get_price(base, quote, amount)
        text = f"Цена {amount} {base} в {quote}: {total}"
        bot.reply_to(message, text)
    
    except APIException as e:
        bot.reply_to(message, f"Ошибка: {e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать запрос: {e}")

bot.polling()
