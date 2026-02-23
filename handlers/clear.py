from aiogram import Router, types
from aiogram.filters import Command

from db import get_session
from tables import User, Task

router = Router()

@router.message(Command("clear"))
async def clear(message: types.Message):
    with get_session() as session:
        tasks = session.query(Task)\
                       .filter(Task.user_id == message.from_user.id)\
                       .order_by(Task.id).all()

        if tasks:
            session.query(Task).filter(Task.user_id == message.from_user.id).delete()

            user = session.query(User).filter_by(id=message.from_user.id).first()
            if not user:
                await message.answer("🤖 Сначала тебе нужно познакомиться со мной.\nНапиши /start!")
                return

            user.deleted = user.deleted + len(tasks)
            
            await message.answer("🧹 Чистота! Ты очистил свой список задач.")
        else:
            await message.answer("☕️ У тебя и так всё чисто.")
