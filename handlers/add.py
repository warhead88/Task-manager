from aiogram import Router, types
from aiogram.filters import Command

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from db import get_session
from tables import Task

router = Router()

class Form(StatesGroup):
    waiting_for_text = State()

@router.message(Command("add"))
async def add_task(message: types.Message, state: FSMContext):
    await state.set_state(Form.waiting_for_text)
    await message.answer("Введи задачу:")

@router.message(Form.waiting_for_text)
async def process_text(message: types.Message, state: FSMContext):
    task_text = message.text

    await state.update_data(task=task_text)

    with get_session() as session:
        new_task = Task(user_id=message.from_user.id, description=task_text)
        session.add(new_task)

    await message.answer("Задача сохранена.")
    await state.clear()
