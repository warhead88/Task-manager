from aiogram import Router, types
from aiogram.filters import Command

from src.db import get_session
from src.tables import User

router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    with get_session() as session:
        user = session.query(User).filter_by(id=message.from_user.id).first()
        if not user:
            user = User(id=message.from_user.id, completed=0, deleted=0)
            session.add(user)
            await message.answer("✨ Привет! Я твой персональный Таск-менеджер.\n\nНапиши /help, чтобы узнать, что я умею.")
        else:
            await message.answer("📝 Ты уже в системе! Если забыл команды, просто набери /help.")
