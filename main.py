import telebot
import sqlite3
import re
from datetime import datetime, timedelta

token = ''
bot = telebot.TeleBot(token)

db_path = "C:\\Users\\Limzor\\Desktop\\GitTele\\TulaHack_Two_2.3\\attractions.db"
conn = sqlite3.connect(db_path, check_same_thread=False)  # добавлено check_same_thread=False для работы с многопоточностью
cursor = conn.cursor()

userdata = {}
TotalTime = {}

HELP = """
/help список команд
/restart перезапустить бота
/start начать сессию"""

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Введите временной промежуток в формате HH:MM-HH:MM")

def parse_time_range(time_range):
    match = re.match(r'(\d{2}):(\d{2})-(\d{2}):(\d{2})', time_range)
    if not match:
        raise ValueError("Invalid time range format. Expected format: HH:MM-HH:MM")
    start_hour, start_minute, end_hour, end_minute = map(int, match.groups())
    start_time = datetime.strptime(f"{start_hour:02}:{start_minute:02}", '%H:%M').time()
    end_time = datetime.strptime(f"{end_hour:02}:{end_minute:02}", '%H:%M').time()
    return start_time, end_time

def calculate_duration(start_time, end_time):
    start_datetime = datetime.combine(datetime.today(), start_time)
    end_datetime = datetime.combine(datetime.today(), end_time)
    if end_datetime < start_datetime:
        end_datetime += timedelta(days=1)  # В случае если время пересекает полночь
    duration = end_datetime - start_datetime
    return duration

def is_open_during(time_range, open_time, close_time):
    start_time, end_time = parse_time_range(time_range)
    open_time = datetime.strptime(open_time, '%H:%M').time()
    close_time = datetime.strptime(close_time, '%H:%M').time()
    
    if close_time < open_time:  # В случае если время пересекает полночь
        close_time = (datetime.combine(datetime.today(), close_time) + timedelta(days=1)).time()
    
    return open_time <= start_time and end_time <= close_time

@bot.message_handler(func=lambda message: True)
def handle_time_range(message):
    user_time_range = message.text
    user_id = message.chat.id
    try:
        start_time, end_time = parse_time_range(user_time_range)
        duration = calculate_duration(start_time, end_time)
        TotalTime[user_id] = duration

        cursor.execute('SELECT name, open_time, close_time FROM attractions')
        available_attractions = []
        for row in cursor.fetchall():
            name, open_time, close_time = row
            if is_open_during(user_time_range, open_time, close_time):
                available_attractions.append(name)
        if available_attractions:
            bot.send_message(message.chat.id, f"Доступные места: {', '.join(available_attractions)}")
        else:
            bot.send_message(message.chat.id, "Нет доступных мест в указанное время")

        bot.send_message(message.chat.id, f"Разница во времени: {duration}")

    except ValueError as e:
        bot.send_message(message.chat.id, str(e))

bot.polling(none_stop=True)
