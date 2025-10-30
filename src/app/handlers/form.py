from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


router = Router()

class UserForm(StatesGroup):
    name = State()
    age = State()
    city = State()


@router.message(Command("start_form"))
async def start_form(message: types.Message, state: FSMContext):
    await message.answer("Как тебя зовут?")
    await state.set_state(UserForm.name)


@router.message(UserForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(UserForm.age)


@router.message(UserForm.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Из какого ты города?")
    await state.set_state(UserForm.city)

@router.message(UserForm.city)
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    data = await state.get_data()
    await message.answer(
        f"✅ Анкета завершена!\n"
        f"Имя: {data['name']}\nВозраст: {data['age']}\nГород: {data['city']}"
    )
    await state.clear()