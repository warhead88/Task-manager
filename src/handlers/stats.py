from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.future import select

from src.db import get_session
from src.tables import User


router = Router()


@router.message(Command("stats"))
async def show_stats(message: types.Message):
    async with get_session() as session:
        result = await session.execute(select(User).filter_by(id=message.from_user.id))
        user = result.scalars().first()

        await message.answer(
            f"📊 *Твои достижения:*\n\n"
            f"✅ Выполнил задач: {user.completed}\n"
            f"🗑 Удалил задач: {user.deleted}\n"
            f"🌍 Часовой пояс: *UTC {user.timezone:+}*",
            parse_mode="Markdown"
        )
