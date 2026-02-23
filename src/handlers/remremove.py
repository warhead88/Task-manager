from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.future import select
from src.db import get_session
from src.tables import Task


router = Router()


@router.message(Command("remremove"))
async def remove_reminder(message: types.Message):
    try:
        index = int(message.text.split()[1]) - 1
    except (IndexError, ValueError):
        await message.answer(
            "⚠️ Используй команду так: `/remremove 1` (где 1 — номер задачи из списка /remlist)",
            parse_mode="Markdown"
        )
        return

    async with get_session() as session:
        result = await session.execute(
            select(Task).filter(
                Task.user_id == message.from_user.id,
                Task.remind_at.is_not(None)
            ).order_by(Task.remind_at)
        )
        tasks = result.scalars().all()

        if 0 <= index < len(tasks):
            task = tasks[index]
            desc = task.description
            task.remind_at = None
            task.recurrence = "none"
            await message.answer(f"🔕 Напоминание для задачи *{desc}* удалено.", parse_mode="Markdown")
        else:
            await message.answer("❓ В списке напоминаний нет задачи под таким номером. Проверь /remlist.")
