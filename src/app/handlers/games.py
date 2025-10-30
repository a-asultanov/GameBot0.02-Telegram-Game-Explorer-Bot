from aiogram import Router, types, F
from src.app.keyboards.inline_games import game_menu, details_inline, get_genre_keyboard, get_year_keyboard, get_platform_keyboard
from src.app.handlers.form import UserForm
from aiogram.fsm.context import FSMContext
from src.app.services.game_service import get_top_games, get_game_details, get_games_by_genre_and_year
import random
import aiohttp


router = Router()

@router.message(lambda m: m.text == "🎮 Каталог игр")
async def show_games(message: types.Message):
    await message.answer("Выбери действие:", reply_markup=game_menu)


@router.callback_query(F.data == "top_games")
async def choose_platform(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Выбери платформу 💻",
        reply_markup=get_platform_keyboard()
    )

@router.callback_query(F.data.startswith("platform:"))
async def choose_genre(callback: types.CallbackQuery, state: FSMContext):
    platform = callback.data.split(":")[1]
    await state.update_data(selected_platform=platform)

    await callback.message.edit_text(
        "Теперь выбери жанр 🎮",
        reply_markup=get_genre_keyboard()
    )

@router.callback_query(F.data.startswith("year:"))
async def show_top_games(callback: types.CallbackQuery, state: FSMContext):
    year = callback.data.split(":")[1]
    data = await state.get_data()
    genre = data.get("selected_genre")
    platform = data.get("selected_platform")
     
    user_id = callback.from_user.id
    username = callback.from_user.username or "unknown"

    url = (
        f"http://127.0.0.1:5000/api/games/top?"
        f"genre={genre}&year={year}&platform={platform}"
        f"&user_id={user_id}&username={username}"
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await callback.message.answer("⚠️ Ошибка при запросе к серверу.")
                return
            result = await response.json()

    games = result.get("games", [])
    if not games:
        await callback.message.answer("😔 Нет игр по этим фильтрам.")
        return

    random_games = random.sample(games, 5) if len(games) >= 5 else games

    for game in random_games:
        url = f"https://rawg.io/games/{game['slug']}"
        image = game.get("background_image")
        caption = (
            f"🎮 <b><a href='{url}'>{game['name']}</a></b>\n"
            f"⭐ {game['rating']} | 📅 {game['released']}"
        )

        if image:
            try:
                await callback.message.answer_photo(
                    photo=image,
                    caption=caption,
                    parse_mode="HTML",
                    disable_web_page_preview=True,
                    reply_markup=details_inline(game["slug"])
                )
            except Exception:
                await callback.message.answer(
                    caption,
                    parse_mode="HTML",
                    disable_web_page_preview=True,
                    reply_markup=details_inline(game["slug"])
                )
        else:
            await callback.message.answer(
                caption,
                parse_mode="HTML",
                disable_web_page_preview=True
            )

    await callback.answer()

@router.callback_query(F.data.startswith("genre:"))
async def choose_year(callback: types.CallbackQuery, state: FSMContext):
    genre = callback.data.split(":")[1]
    await state.update_data(selected_genre=genre)

    await callback.message.edit_text(
        "Теперь выбери год 🗓️",
        reply_markup=get_year_keyboard()
    )    


@router.callback_query(lambda c: c.data.startswith("details_"))
async def show_game_details(callback: types.CallbackQuery):
    slug = callback.data.split("details_")[1]
    await callback.answer("Загружаю описание...")

    game = await get_game_details(slug)

    name = game.get("name")
    rating = game.get("rating")
    released = game.get("released") or "TBA"
    desc = game.get("description_raw") or "Описание отсутствует 😕"
    image = game.get("background_image")
    url = f"https://rawg.io/games/{slug}"


    # Формируем карточку
    text = (
        f"🎮 <b><a href='{url}'>{name}</a></b>\n"
        f"⭐ {rating} | 📅 {released}\n\n"
        f"{desc[:700]}..."
    )

    # Отправляем карточку пользователю
    if image:
        await callback.message.answer_photo(
            photo=image,
            caption=text,
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    else:
        await callback.message.answer(
            text,
            parse_mode="HTML",
            disable_web_page_preview=True
        )



@router.callback_query(F.data == "random_game")
async def send_random_game(callback: types.callback_query):
    await callback.message.answer("🎲 Случайная игра: Minecraft 😄")
    await callback.answer()

@router.callback_query(lambda c: c.data == "user_form")
async def fill_out_form(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Как тебя зовут?")
    await state.set_state(UserForm.name)
    await callback.answer()
