import telebot

token = '6816672868:AAGokrUKgeGlCjnbXVpnEXM_eiuHQxsKseg'

bot = telebot.TeleBot(token)

HELP = """
/help список команд
/restart перезапустить бота
/start начать сессию"""

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(content_types=["text"])
def echo(message):
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)