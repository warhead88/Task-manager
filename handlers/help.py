from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def show_help(message: types.Message):
    await message.answer("""Команды:

1. list - показывает список задач;
2. add - добавляет задачу в список (для использования нужно сначала просто написать add, а после ответа бота писать саму задачу);
3. remove - удаляет задачу из списка;
4. done - помечает задачу выполненной и удаляет из списка;
5. clear - очищает список задач;
6. stats - показывает статистику;
7. help - показывает список команд;
8. cancel - отменяет текущее действие.

Приятного пользования!""")
