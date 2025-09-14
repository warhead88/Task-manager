from aiogram import Router, types
from aiogram.filters import Command

from db import get_session
from tables import User, Task

router = Router()

@router.message(Command("remove"))
async def remove_task(message: types.Message):
    try:
        index = int(message.text.split()[1]) - 1
    except (IndexError, ValueError):
        await message.answer("Введён неверный формат или номер задачи.")
        return

    with get_session() as session:
        tasks = session.query(Task)\
                       .filter(Task.user_id == message.from_user.id)\
                       .order_by(Task.id).all()

        if 0 <= index <= (len(tasks) - 1):
            session.delete(tasks[index])
            await message.answer(f"Задача '{tasks[index].description}' удалена.")
        else:
            await message.answer("Такой задачи нет.")
