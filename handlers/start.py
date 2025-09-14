from aiogram import Router, types
from aiogram.filters import Command

from db import get_session
from tables import User

router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    with get_session() as session:
        user = session.query(User).filter_by(id=message.from_user.id).first()
        if not user:
            user = User(id=message.from_user.id, completed=0, removed=0, cleared=0)
            session.add(user)
            await message.answer("Привет! Это бот Таск-менеджер. Напиши '/help'")
        else:
            await message.answer("Узнать о функционале и командах можно с помощью команды help.")
