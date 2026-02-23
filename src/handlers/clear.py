from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.future import select

from src.db import get_session
from src.tables import User, Task


router = Router()


@router.message(Command("clear"))
async def clear(message: types.Message):
    async with get_session() as session:
        result = await session.execute(
            select(Task)
            .filter(Task.user_id == message.from_user.id)
            .order_by(Task.id)
        )
        tasks = result.scalars().all()

        if tasks:
            for task in tasks:
                await session.delete(task)

            user_result = await session.execute(select(User).filter_by(id=message.from_user.id))
            user = user_result.scalars().first()

            user.deleted = user.deleted + len(tasks)

            await message.answer("🧹 Чистота! Ты очистил свой список задач.")
        else:
            await message.answer("☕️ У тебя и так всё чисто.")
