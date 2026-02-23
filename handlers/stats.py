from aiogram import Router, types
from aiogram.filters import Command

from db import get_session
from tables import User

router = Router()

@router.message(Command("stats"))
async def show_stats(message: types.Message):
    with get_session() as session:
        user = session.query(User).filter_by(id=message.from_user.id).first()

        if not user:
            await message.answer("Пожалуйста, напишите /start для регистрации.")
            return

        deleted = user.deleted
        completed = user.completed

    await message.answer(f"Ваша статистика:\n\nВыполнено задач: {completed};\nУдалено задач: {deleted}.")
