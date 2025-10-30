from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from src.app.keyboards.main_menu import get_main_menu
router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! 🎮",
        reply_markup=get_main_menu()
    )

@router.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("Просто жми на кнопки! Ха-ха 😉")

@router.message(lambda m: m.text == "ℹ️ Помощь")
async def help_button(message: types.Message):
    await help_command(message)