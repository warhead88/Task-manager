import asyncio
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot

from src.db import get_session
from src.tables import Task

async def check_reminders(bot: Bot):
    now = datetime.utcnow()
    with get_session() as session:
        tasks = session.query(Task).filter(Task.remind_at != None, Task.remind_at <= now).all()
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
            if task.recurrence == "none":
                task.remind_at = None
            else:
                next_remind = task.remind_at
                while True:
                    if task.recurrence == "daily":
                        next_remind += timedelta(days=1)
                    elif task.recurrence == "weekdays":
                        next_remind += timedelta(days=1)
                        if next_remind.weekday() >= 5:
                            continue
                    elif task.recurrence == "weekends":
                        next_remind += timedelta(days=1)
                        if next_remind.weekday() < 5:
                            continue
                    elif task.recurrence == "weekly":
                        next_remind += timedelta(days=7)
                    
                    # Stop if next_remind is in the future
                    if next_remind > now:
                        break
                
                task.remind_at = next_remind

def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_reminders, 'interval', minutes=1, args=[bot])
    scheduler.start()
    return scheduler
