import sqlite3
from geopy.distance import geodesic

db_path = "C:\\Users\\User\\Desktop\\gittele\\attractions.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Получение координат пользователя(указал ул.Грибоедова, д.54)
user_latitude = 54.099649
user_longitude = 37.582038

# Получение всех координат мест
cursor.execute('SELECT id, name, Shirota, Dolgota FROM attractions')
attractions = cursor.fetchall()

# Создание списка с расстояниями от каждого места до пользователя
distances = []
for place in attractions:
    distance = geodesic((user_latitude, user_longitude), (place[2], place[3])).km
    distances.append((place[0], place[1], distance))

# Сортировка мест по расстоянию
sorted_places = sorted(distances, key=lambda x: x[2])

# Вывод результатов
for place in sorted_places:
    print(f"{place[1]} - расстояние: {place[2]:.2f} км")

cursor.close()
conn.close()