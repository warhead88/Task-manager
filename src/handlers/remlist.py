from datetime import timedelta
from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.future import select
from src.db import get_session
from src.tables import Task, User


router = Router()


@router.message(Command("remlist"))
async def list_reminders(message: types.Message):
    async with get_session() as session:
        user_result = await session.execute(select(User).filter_by(id=message.from_user.id))
        user = user_result.scalars().first()
        tz_offset = user.timezone if user else 0

        tasks_result = await session.execute(
            select(Task).filter(
                Task.user_id == message.from_user.id,
                Task.remind_at.is_not(None)
            ).order_by(Task.remind_at)
        )
        tasks = tasks_result.scalars().all()

        if not tasks:
            await message.answer("🔔 У тебя нет активных напоминаний.")
            return

        rec_texts = {
            "none": "Один раз",
            "daily": "Каждый день",
            "weekdays": "По будням",
            "weekends": "По выходным",
            "weekly": "Раз в неделю"
        }

        text = f"⏰ *Твои активные напоминания (UTC {tz_offset:+}):*\n\n"
        for i, task in enumerate(tasks, start=1):
            # Convert UTC back to local for display
            local_time = task.remind_at + timedelta(hours=tz_offset)
            time_str = local_time.strftime("%H:%M")
            rec_str = rec_texts.get(task.recurrence, "Неизвестно")
            text += f"{i}. *{task.description}*\n   └ 🕒 {time_str} — {rec_str}\n\n"

        await message.answer(text, parse_mode="Markdown")
