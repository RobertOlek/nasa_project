import aiohttp

# api
NASA_IMAGE_API_URL = "https://images-api.nasa.gov/search"

# pobieranie danych z api (asynchronicznie)
async def fetch_from_nasa(query):
    # symulacja uzytkownika
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # zapytanie do API,fraza (query) i obrazek
    params = {
        "q": query,
        "media_type": "image"
    }

    # Tworzym sesje i wysyła zapytanie
    async with aiohttp.ClientSession() as session:
        async with session.get(NASA_IMAGE_API_URL, params=params, headers=headers) as response:
            # zapytanie dziala lub nie
            if response.status != 200:
                print(f"nie działa api: {response.status}")
                return []

            # jesli działa, idziemy dalej
            data = await response.json()
            items = data.get("collection", {}).get("items", [])

            # przechowywanie przerobionych wyników
            results = []
            for item in items:
                data_item = item.get("data", [])[0]
                title = data_item.get("title", "Brak tytułu")
                description = data_item.get("description", "Brak opisu")
                nasa_id = data_item.get("nasa_id", "")

                # Pobieranie linku do obrazka
                links = item.get("links", [])
                image_url = links[0]["href"] if links else ""

                # Dodaje wynik do listy
                results.append({
                    "name": title,
                    "description": description,
                    "nasa_id": nasa_id,
                    "image_url": image_url
                })

            # Zwraca obrobione wyniki
            return results
