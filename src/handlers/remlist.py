from aiogram import Router, types
from aiogram.filters import Command
from src.db import get_session
from src.tables import Task

router = Router()

@router.message(Command("remlist"))
async def list_reminders(message: types.Message):
    with get_session() as session:
        tasks = session.query(Task).filter(
            Task.user_id == message.from_user.id,
            Task.remind_at != None
        ).order_by(Task.remind_at).all()

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

        text = "⏰ *Твои активные напоминания:*\n\n"
        for i, task in enumerate(tasks, start=1):
            time_str = task.remind_at.strftime("%H:%M (UTC)")
            rec_str = rec_texts.get(task.recurrence, "Неизвестно")
            text += f"{i}. *{task.description}*\n   └ 🕒 {time_str} — {rec_str}\n\n"

        await message.answer(text, parse_mode="Markdown")
