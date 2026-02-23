from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.future import select

from src.db import get_session
from src.tables import Task, User


router = Router()


@router.message(Command("done"))
async def make_done(message: types.Message):
    try:
        index = int(message.text.split()[1]) - 1
    except (IndexError, ValueError):
        await message.answer("⚠️ Похоже, ты ввёл неверный номер или формат.\nПопробуй так: `/done 1`", parse_mode="Markdown")
        return

    async with get_session() as session:
        result = await session.execute(
            select(Task)
            .filter(Task.user_id == message.from_user.id)
            .order_by(Task.id)
        )
        tasks = result.scalars().all()

        if 0 <= index <= (len(tasks) - 1):
            completed_desc = tasks[index].description
            await session.delete(tasks[index])

            user_result = await session.execute(select(User).filter_by(id=message.from_user.id))
            user = user_result.scalars().first()

            user.completed = user.completed + 1

            await message.answer(f"🎉 Поздравляю! Ты выполнил задачу: *{completed_desc}*", parse_mode="Markdown")
        else:
            await message.answer("❓ У тебя нет задачи под таким номером.")
