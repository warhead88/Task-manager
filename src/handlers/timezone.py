from aiogram import Router, types
from aiogram.filters import Command
from src.db import get_session
from src.tables import User

router = Router()

@router.message(Command("timezone"))
async def set_timezone(message: types.Message):
    args = message.text.split()
    if len(args) != 2:
        await message.answer(
            "🌍 *Настройка часового пояса*\n\n"
            "Пожалуйста, укажи смещение от UTC. Например:\n"
            "`/timezone +3` (для Москвы)\n"
            "`/timezone -5` (для Нью-Йорка)\n\n"
            "Текущие настройки можно проверить через /stats.",
            parse_mode="Markdown"
        )
        return

    try:
        offset = int(args[1].replace("+", ""))
        if not (-12 <= offset <= 14):
            raise ValueError()
    except ValueError:
        await message.answer("⚠️ Пожалуйста, введи целое число от -12 до +14.")
        return

    with get_session() as session:
        user = session.query(User).filter_by(id=message.from_user.id).first()
        if user:
            user.timezone = offset
            await message.answer(f"✅ Часовой пояс успешно установлен: *UTC {offset:+}*", parse_mode="Markdown")
        else:
            await message.answer("❌ Ошибка: пользователь не найден. Попробуй /start")
