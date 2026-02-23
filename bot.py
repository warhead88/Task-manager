import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import Config
from db import init_db
from handlers import start, add, remove, ls, done, clear, stats, help, echo
from middlewares import RegistrationMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

async def main():
    init_db()
    
    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher()
    
    dp.message.middleware(RegistrationMiddleware())

    dp.include_router(start.router)
    dp.include_router(add.router)
    dp.include_router(remove.router)
    dp.include_router(ls.router)
    dp.include_router(done.router)
    dp.include_router(clear.router)
    dp.include_router(stats.router)
    dp.include_router(help.router)
    dp.include_router(echo.router)  # Этот роутер должен быть последним

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
