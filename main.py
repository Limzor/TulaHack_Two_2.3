# Импорт необходимых модулей
import telebot
import sqlite3
import re
from datetime import datetime, timedelta

# Токен для бота
token = ''

# Создание экземпляра бота
bot = telebot.TeleBot(token)

# Путь к базе данных
db_path = "attractions.db"

# Подключение к базе данных
conn = sqlite3.connect(db_path, check_same_thread=False)  # Добавлено check_same_thread=False для работы с многопоточностью
cursor = conn.cursor()

# Словари для хранения данных пользователей и общего времени
userdata = {}
TotalTime = {}

# Строка помощи
HELP = """
/help список команд
/restart перезапустить бота
/start начать сессию"""

# Обработчик команды /help
@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)

# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Введите временной промежуток в формате HH:MM-HH:MM")

# Функция для разбора временного диапазона
def parse_time_range(time_range):
    match = re.match(r'(\d{2}):(\d{2})-(\d{2}):(\d{2})', time_range)
    if not match:
        raise ValueError("Неправильный формат. Укажите формат следующим образом: HH:MM-HH:MM")
    start_hour, start_minute, end_hour, end_minute = map(int, match.groups())
    start_time = datetime.strptime(f"{start_hour:02}:{start_minute:02}", '%H:%M').time()
    end_time = datetime.strptime(f"{end_hour:02}:{end_minute:02}", '%H:%M').time()
    return start_time, end_time

# Функция для расчета продолжительности периода
def calculate_duration(start_time, end_time):
    start_datetime = datetime.combine(datetime.today(), start_time)
    end_datetime = datetime.combine(datetime.today(), end_time)
    if end_datetime < start_datetime:
        end_datetime += timedelta(days=1)  # В случае если время пересекает полночь
    duration = end_datetime - start_datetime
    return duration

# Функция для проверки открыто ли место в указанный период времени
def is_open_during(time_range, open_time, close_time):
    start_time, end_time = parse_time_range(time_range)
    open_time = datetime.strptime(open_time, '%H:%M').time()
    close_time = datetime.strptime(close_time, '%H:%M').time()
    
    if close_time < open_time:  # В случае если время пересекает полночь
        close_time = (datetime.combine(datetime.today(), close_time) + timedelta(days=1)).time()
    
    return open_time <= start_time and end_time <= close_time

# Обработчик сообщений для обработки временных диапазонов
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

# Запуск бесконечного опроса обновлений от Telegram
bot.polling(none_stop=True)
