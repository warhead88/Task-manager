from aiogram import Router, types
from aiogram.filters import Command

from src.db import get_session
from src.tables import User, Task

router = Router()

@router.message(Command("remove"))
async def remove_task(message: types.Message):
    try:
        index = int(message.text.split()[1]) - 1
    except (IndexError, ValueError):
        await message.answer("⚠️ Похоже, ты ввёл неверный номер или формат.\nПопробуй так: `/remove 1`", parse_mode="Markdown")
        return

    with get_session() as session:
        tasks = session.query(Task)\
                       .filter(Task.user_id == message.from_user.id)\
                       .order_by(Task.id).all()

        if 0 <= index <= (len(tasks) - 1):
            deleted_desc = tasks[index].description
            session.delete(tasks[index])

            user = session.query(User).filter_by(id=message.from_user.id).first()
            
            user.deleted = user.deleted + 1

            await message.answer(f"🗑 Ты удалил задачу: *{deleted_desc}*", parse_mode="Markdown")
        else:
            await message.answer("❓ У тебя нет задачи под таким номером.")
