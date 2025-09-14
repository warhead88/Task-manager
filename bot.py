import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import Config
from db import init_db
from handlers import start, add, remove, ls, done, clear, stats

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

init_db()

async def main():
    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(add.router)
    dp.include_router(remove.router)
    dp.include_router(ls.router)
    dp.include_router(done.router)
    dp.include_router(clear.router)
    dp.include_router(stats.router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
