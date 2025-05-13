import sqlite3
from sqlite3 import Error

# łączenie z bazą
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)  # Łączenie z bazą
        print(f"Połączenie działa. Wersja: {sqlite3.version}")
    except Error as e:
        print(f"Błąd połączenia: {e}")
    return conn

# tworzenie tabeli, jeśli nie ma
def create_table(conn):
    try:
        create_table_sql = '''
            CREATE TABLE IF NOT EXISTS space_objects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  # Unikalny ID dla każdego obiektu
                query TEXT,  # Zapytanie użytkownika
                name TEXT NOT NULL,  # Nazwa ciała niebieskiego
                description TEXT,  # Opis ciała niebieskiego
                nasa_id TEXT,  # ID z NASA
                image_url TEXT,  # Link do obrazu
                title TEXT  # Tytuł ciała niebieskiego
            );
        '''
        cursor = conn.cursor()
        cursor.execute(create_table_sql)  # Wykonanie zapytania tworzącego tabelę
        print("Tabela 'space_objects' została utworzona.")
    except Error as e:
        print(f"Błąd podczas tworzenia tabeli: {e}")

# wstawianie danych do tabeli
def insert_object(conn, name, description, image_url=None, query=None, nasa_id=None, title=None):
    try:
        insert_sql = '''
            INSERT INTO space_objects (name, description, image_url, query, nasa_id, title)
            VALUES (?, ?, ?, ?, ?, ?);
        '''
        cursor = conn.cursor()
        cursor.execute(insert_sql, (name, description, image_url, query, nasa_id, title))  # Wstawianie danych do tabeli
        conn.commit()  # Zatwierdzenie
        print("dodano do bazy.")
    except Error as e:
        print(f"Błąd przy wstawianiu danych: {e}")

# aktualizacja danych w tabeli
def update_object(conn, old_name, new_name=None, description=None, image_url=None):
    try:
        update_sql = "UPDATE space_objects SET"
        updates = []  # Lista z aktualizacjami
        params = []  # Parametry do zapytania SQL

        # Dodawanie nowych danych, jesli zostały podane
        if new_name:
            updates.append(" name = ?")
            params.append(new_name)
        if description:
            updates.append(" description = ?")
            params.append(description)
        if image_url:
            updates.append(" image_url = ?")
            params.append(image_url)

        if not updates:
            print("Brak danych do aktualizacji.")
            return

        update_sql += ",".join(updates) + " WHERE name = ?;"
        params.append(old_name)

        cursor = conn.cursor()
        cursor.execute(update_sql, tuple(params))  #  zapytanie aktualizującego
        conn.commit()  # Zatwierdzenie
        print("Dane zaktualizowane.")
    except Error as e:
        print(f"Błąd przy aktualizacji danych: {e}")

# usuwanie obiektu z bazy danych (delete) (działa)
def delete_object(conn, name_query):
    try:
        cursor = conn.cursor()
        print(f"Sprawdzanie przed usunięciem: {name_query}")

        # Szukanie pasujących rekordów w wielu kolumnach
        cursor.execute("""
            SELECT id, name FROM space_objects
            WHERE name LIKE ?
               OR description LIKE ?
               OR title LIKE ?
               OR query LIKE ?
               OR nasa_id LIKE ?
               OR image_url LIKE ?
        """, tuple(['%' + name_query + '%'] * 6))
        rows_before = cursor.fetchall()

        if rows_before:
            print("Dane do usunięcia:", rows_before)
        else:
            print("Nie znaleziono danych do usunięcia.")

        # Usuwamy rekordy pasujące do frazy w wielu kolumnach
        cursor.execute("""
            DELETE FROM space_objects
            WHERE name LIKE ?
               OR description LIKE ?
               OR title LIKE ?
               OR query LIKE ?
               OR nasa_id LIKE ?
               OR image_url LIKE ?
        """, tuple(['%' + name_query + '%'] * 6))
        conn.commit()
        print(f"Dane zostały usunięte: {name_query}")

        cursor.execute("VACUUM")
        conn.commit()

        # Sprawdzenie po usunięciu
        cursor.execute("""
            SELECT id, name FROM space_objects
            WHERE name LIKE ?
               OR description LIKE ?
               OR title LIKE ?
               OR query LIKE ?
               OR nasa_id LIKE ?
               OR image_url LIKE ?
        """, tuple(['%' + name_query + '%'] * 6))
        rows_after = cursor.fetchall()

        if rows_after:
            print("Dane po usunięciu (nadal istnieją):", rows_after)
        else:
            print("dane zostały usunięte.")

        conn.close()
        print("Połączenie z bazą zamknięte.")

    except Error as e:
        print(f"Błąd przy usuwaniu: {e}")


# wyszukiwanie w bazie
def search_objects(conn, query):
    try:
        search_sql = '''SELECT * FROM space_objects
                        WHERE name LIKE ?
                           OR description LIKE ?
                           OR title LIKE ?;'''  # Szukanie w kolumnach name, description, title
        cursor = conn.cursor()
        cursor.execute(search_sql, (f"%{query}%", f"%{query}%", f"%{query}%"))
        return cursor.fetchall()  # Zwracamy wszystkie pasujące wiersze
    except Error as e:
        print(f"Błąd przy wyszukiwaniu: {e}")
        return []
