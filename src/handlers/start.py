from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.future import select

from src.db import get_session
from src.tables import User

router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    async with get_session() as session:
        result = await session.execute(select(User).filter_by(id=message.from_user.id))
        user = result.scalars().first()
        
        if not user:
            user = User(id=message.from_user.id, completed=0, deleted=0)
            session.add(user)
            await message.answer("✨ Привет! Я твой персональный Таск-менеджер.\n\nНапиши /help, чтобы узнать, что я умею.")
        else:
            await message.answer("📝 Ты уже в системе! Если забыл команды, просто набери /help.")
