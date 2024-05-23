import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('attractions.db')
c = conn.cursor()

# Create a table for storing attractions
c.execute('''CREATE TABLE IF NOT EXISTS attractions (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                work_hours TEXT,
                placement TEXT,
                type TEXT
            )''')

# Commit the changes and close the connection
conn.commit()
conn.close()
