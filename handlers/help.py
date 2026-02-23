from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def show_help(message: types.Message):
    await message.answer("""🛠 *Что я умею:*

1️⃣ /list — покажу твой список задач
2️⃣ /add — помогу тебе записать новую задачу (просто напиши команду, а потом текст задачи)
3️⃣ /remove — удалю задачу по её номеру (например: `/remove 1`)
4️⃣ /done — отмечу задачу как выполненную (например: `/done 1`)
5️⃣ /stats — покажу твои успехи в делах
6️⃣ /clear — полностью очищу твой список задач
7️⃣ /help — напомню тебе эти команды

✨ *Удачи в делах!*""", parse_mode="Markdown")
