from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

game_menu = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text="🔥 Топ игр", callback_data="top_games")]#,
        #[InlineKeyboardButton(text="🎲 Во что поиграть?", callback_data="random_game")]#,
        #[InlineKeyboardButton(text="Заполнить анкету 😃", callback_data="user_form")]
    ]
)

def details_inline(slug: str):
    return InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(text="Подробнее...", callback_data=f"details_{slug}")]
        ]
    )

def get_platform_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row_width = 2

    platforms = [
        ("💻 PC", "4"),
        ("🎮 PlayStation", "18"),
        ("🎮 Xbox", "1"),
        ("📱 Android", "21"),
    ]

    for name, platform_id in platforms:
        builder.button(text=name, callback_data=f"platform:{platform_id}")

    builder.adjust(2)
    return builder.as_markup()


def get_genre_keyboard():

    builder = InlineKeyboardBuilder()
    builder.row_width = 2

    genres = [
    ("🎯 Action", "action"),
    ("⚔️ RPG", "role-playing-games-rpg"),
    ("🧩 Puzzle", "puzzle"),
    ("🕵️ Adventure", "adventure"),
    ("🚗 Racing", "racing"),
    ("🧙 Fantasy", "fantasy"),
    ("🧠 Strategy", "strategy"),
    ("😱 Horror", "horror")
]

    for name, genre in genres:
        builder.button(text=name, callback_data=f"genre:{genre}")
    builder.adjust(2)
    return builder.as_markup()

def get_year_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row_width = 2

    years = [2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018]

    for year in years:
        builder.button(text=str(year), callback_data=f"year:{year}")
    builder.adjust(2)
    return builder.as_markup()