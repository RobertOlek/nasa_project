import sqlite3

# Połączenie
conn = sqlite3.connect('space_objects.db')
cursor = conn.cursor()

# Dodanie kolumny
cursor.execute("ALTER TABLE space_objects ADD COLUMN title TEXT")

# Zatwierdzenie
conn.commit()

# Zamknięcie
conn.close()
