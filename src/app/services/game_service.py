import asyncio
import aiohttp
import os
from dotenv import load_dotenv

CACHE = {}
load_dotenv()
RAWG_API_KEY = os.getenv("RAWG_API_KEY")

async def get_top_games():
    url = "https://api.rawg.io/api/games"
    params = {
        "key": RAWG_API_KEY,
        "ordering": "-rating,-added",
        "platforms": 4,
        "dates": "2025-01-01,2025-12-31",
        "page_size": 20
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            return data["results"]


async def get_game_details(slug: str):
    url = f"https://api.rawg.io/api/games/{slug}"
    params = {"key": RAWG_API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            return data



async def get_games_by_genre_and_year(genre: str, year: str, platform: str):
    # Проверяем, есть ли уже данные в кэше
    cache_key = (genre, year)
    if cache_key in CACHE:
        return CACHE[cache_key]

    # Формируем URL запроса
    url = "https://api.rawg.io/api/games"
    params = {
        "key": RAWG_API_KEY,
        "genres": genre,
        "dates": f"{year}-01-01,{year}-12-31",
        "ordering": "-rating,-added",
        "page_size": 50,
        "platforms": platform
    }


    # Делаем запрос к API
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    print(f"⚠️ RAWG API error: {response.status}")
                    return []
                data = await response.json()
    except Exception as e:
        print(f"⚠️ Ошибка при запросе к RAWG: {e}")
        return []
    # Забираем список игр
    games = data.get("results", [])
    if year == "2025":
        games = [
            g for g in games
            if g.get("background_image") and g.get("released")
        ]
    else:
        games = [
            g for g in games
            if g.get("rating", 0) >= 2.0 and g.get("background_image") and g.get("released")
        ]

    # Сохраняем в кэш
    CACHE[cache_key] = games

    return games