from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.future import select

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

    async with get_session() as session:
        result = await session.execute(
            select(Task)
            .filter(Task.user_id == message.from_user.id)
            .order_by(Task.id)
        )
        tasks = result.scalars().all()

        if 0 <= index <= (len(tasks) - 1):
            deleted_desc = tasks[index].description
            await session.delete(tasks[index])

            user_result = await session.execute(select(User).filter_by(id=message.from_user.id))
            user = user_result.scalars().first()

            user.deleted = user.deleted + 1

            await message.answer(f"🗑 Ты удалил задачу: *{deleted_desc}*", parse_mode="Markdown")
        else:
            await message.answer("❓ У тебя нет задачи под таким номером.")
