from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from src.db import get_session
from src.tables import User

class RegistrationMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        # Пропускаем команду /start, чтобы пользователь мог зарегистрироваться
        if event.text and event.text.startswith("/start"):
            return await handler(event, data)

        with get_session() as session:
            user = session.query(User).filter_by(id=event.from_user.id).first()
            
        if not user:
            await event.answer(
                "🤖 *Ой! Кажется, мы ещё не знакомы.*\n\n"
                "Чтобы я мог запоминать твои задачи, пожалуйста, нажми или напиши /start",
                parse_mode="Markdown"
            )
            return

        return await handler(event, data)
