import telebot
from config import keys, TOKEN
from extensions import APIExeprion, ValutesConveter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Привет✌, чтобы начать работу бота, введи команду в следующем порядке:\n<название валюты> \
<в какую валюту перевести>\
<количество переводимой валюты>\nЧтобы увидеть список всех доступных валют для конвертации используй команду: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split()

        if len(values) != 3:
          raise APIExeprion('Слишком много параметров.')

        quote, base, amount = values
        get_price = ValutesConveter.convert(quote, base, amount)
    except APIExeprion as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'цена {amount} {quote} в {base} - {get_price * float(amount)}'
        bot.send_message(message.chat.id, text)


bot.polling()
