from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.future import select

from src.db import get_session
from src.tables import Task

router = Router()


@router.message(Command("list"))
async def show_tasks(message: types.Message):
    async with get_session() as session:
        result = await session.execute(
            select(Task)
            .filter(Task.user_id == message.from_user.id)
            .order_by(Task.id)
        )
        tasks = result.scalars().all()

        if tasks:
            text = "📋 *Твой список задач:*\n\n" + "\n".join(
                f"{i}. {task.description}" for i, task in enumerate(tasks, start=1)
            )
            await message.answer(text, parse_mode="Markdown")
        else:
            await message.answer("☕️ Твой список пуст. Отдыхай!")
