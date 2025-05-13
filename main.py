import asyncio
from database import (
    create_connection,
    create_table,
    insert_object,
    update_object,
    delete_object,
    search_objects
)
from nasa_api import fetch_from_nasa

DB_FILE = "space_objects.db"  # baza danych

# Funkcja do wyszukiwania  w db lub w API
async def search():
    query = input("wpisz zapytanie ").strip().lower()

    # Połączenie z bazą
    db_connection = create_connection(DB_FILE)

    # Szukanie w bazie
    print("Szukanie w bazie")
    results = search_objects(db_connection, query)  # wyszukuje obiekt w bazie

    if results:
        print("znalezione w bazie danych:")
        for row in results:
            print(f"- {row[2]}: {row[3]}")  # nazwa i opis
            print(f"  🔗 Obraz: {row[5]}")  # link do obrazu
    else:
        print("Brak wyników w bazie")
        print("szukanie w api")
        api_results = await fetch_from_nasa(query)  # Jeśli brak w bazie, szukamy w api
        if api_results:
            print("znalezione w api:")
            for obj in api_results:
                print(f"- {obj['name']}: {obj['description']}")  # wyniki z API
                print(f"  🔗 Obraz: {obj.get('image_url', 'Brak')}")

                # Zapis do bazy
                insert_object(
                    db_connection,
                    name=obj['name'],
                    description=obj['description'],
                    image_url=obj.get('image_url'),
                    query=query,
                    nasa_id=obj.get('nasa_id'),
                    title=obj.get('title')
                )
        else:
            print("Brak wyników w api.")

    db_connection.close()  # Zamknięcie bazy

# Funkcja usuwania
async def delete():
    query = input("Wpisz nazwę do usuniencia: ").strip().lower()
    db_connection = create_connection(DB_FILE)
    delete_object(db_connection, query)  # Funkcja usuwania
    db_connection.close()

# aktualizuje dane w bazie, enter = brak zmiany
async def update():
    old_name = input(" stara nazwa: ").strip()  # stara nazwa
    new_name = input("nowa nazwa: ").strip()  # nowa nazwa
    new_description = input("nowy opis: ").strip()  # nowy opis
    new_image_url = input("nowy link: ").strip()  # nowy link

    # jesli brak zmiany, zostaje stare
    new_name = new_name if new_name else None
    new_description = new_description if new_description else None
    new_image_url = new_image_url if new_image_url else None

    db_connection = create_connection(DB_FILE)
    update_object(db_connection, old_name, new_name, new_description, new_image_url)  # aktualizuje dane
    db_connection.close()

# działanie aplikacji
async def main():
    print("Działa")
    db_connection = create_connection(DB_FILE)
    create_table(db_connection)  # tworzy tabele jesli nie ma
    db_connection.close()

    while True:
        command = input("\nUzyj komendy (search / delete / update / exit): ").strip().lower()  # Pobranie komendy

        if command == "search":
            await search()  # Wyszukiwanie
        elif command == "delete":
            await delete()  # Usuwanie
        elif command == "update":
            await update()  # Aktualizacja danych
        elif command == "exit":
            print("koniec")
            break  # koniec
        else:
            print("błedne polecenie")  # nieznana komenda

if __name__ == "__main__":
    asyncio.run(main())  # Uruchomienie aplikacji
