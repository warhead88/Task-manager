from aiogram import Router, types
from aiogram.filters import Command

from src.db import get_session
from src.tables import User

router = Router()

@router.message(Command("stats"))
async def show_stats(message: types.Message):
    with get_session() as session:
        user = session.query(User).filter_by(id=message.from_user.id).first()

        deleted = user.deleted
        completed = user.completed

    await message.answer(
        f"📊 *Твои достижения:*\n\n"
        f"✅ Выполнил задач: {completed}\n"
        f"🗑 Удалил задач: {deleted}\n"
        f"🌍 Часовой пояс: *UTC {user.timezone:+}*",
        parse_mode="Markdown"
    )
