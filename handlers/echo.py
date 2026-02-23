from aiogram import Router, types

router = Router()

@router.message()
async def echo_all(message: types.Message):
    await message.answer(
        "🧐 Я не совсем тебя понял.\n\n"
        "Такой команды не существует, или ты ввёл текст просто так.\n"
        "Напиши /help, чтобы увидеть список доступных команд."
    )
