from aiogram import Router, types
from aiogram.filters import Command

from db import get_session
from tables import Task

router = Router()

@router.message(Command("list"))
async def show_tasks(message: types.Message):
    with get_session() as session:
        tasks = session.query(Task)\
                       .filter(Task.user_id == message.from_user.id)\
                       .order_by(Task.id).all()
        
        if tasks:
            text = "Задачи:\n" + "\n".join(
                f"{i}. {task.description}" for i, task in enumerate(tasks, start=1)
            )
            await message.answer(text)
        else:
            await message.answer("У вас нет задач.")
