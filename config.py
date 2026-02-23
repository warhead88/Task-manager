import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./main.db")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set in .env file")
