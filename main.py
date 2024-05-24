import telebot
import sqlite3

token = '6816672868:AAGokrUKgeGlCjnbXVpnEXM_eiuHQxsKseg'

bot = telebot.TeleBot(token)

db_path = "C:\Users\Limzor\Desktop\GitTele\TulaHack_Two_2.3\attractions.db" # Введите актуальный путь до db
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT * FROM attractions")


ELP = """
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