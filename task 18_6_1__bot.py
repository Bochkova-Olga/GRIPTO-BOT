import telebot
from teledram_bot_config import keys, TOKEN
from extensions import APIException, CurrencyConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def help(message: telebot.types.Message):
    text = f'Привет! Я @MyArxiBot. Могу показать список валют: /values \
            \n Помогу сконвертировать валюту. Надо ввести <имя валюты, цену которой вы хотите узнать> \
            \n<имя валюты в которой надо узнать цену первой валюты>  и  <количество первой валюты> \
            \nЕсли не понятно введите команду: /help'

    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = f'Что бы начать работу введите команду боту в следующем формате: \
            \n<имя валюты цену которой вы хотите узнать> <имя валюты в которой надо узнать цену первой валюты> <количество первой валюты> \
            \nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values', ])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key, value in keys.items():
        text = '\n'.join((text, value + " (" + key + ")"))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) > 3:
            raise APIException('Слишком много параметров.')
        elif len(values) < 3:
            raise APIException('Слишком мало параметров.')

        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()