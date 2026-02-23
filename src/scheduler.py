from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from sqlalchemy.future import select

from src.db import get_session
from src.tables import Task
from src.utils import get_next_recurrence_time


async def check_reminders(bot: Bot):
    now = datetime.utcnow()
    async with get_session() as session:
        result = await session.execute(
            select(Task).filter(Task.remind_at.is_not(None), Task.remind_at <= now)
        )
        tasks = result.scalars().all()
        for task in tasks:
            # Send reminder
            try:
                await bot.send_message(
                    chat_id=task.user_id,
                    text=f"🔔 *Напоминание!*\n\n{task.description}",
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Error sending reminder to {task.user_id}: {e}")

            # Update recurrence
            task.remind_at = get_next_recurrence_time(task.remind_at, task.recurrence, now)


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_reminders, 'interval', minutes=1, args=[bot])
    scheduler.start()
    return scheduler
