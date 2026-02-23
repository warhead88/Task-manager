from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from contextlib import asynccontextmanager

from src.tables import Base
from src.config import Config

# Ensure DATABASE_URL uses asyncpg
# E.g. postgresql://user:pass@host/db -> postgresql+asyncpg://user:pass@host/db
async_db_url = Config.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(async_db_url, echo=Config.DEBUG)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

async def init_db():
    async with engine.begin() as conn:
        # Base.metadata.create_all is synchronous, use run_sync
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def get_session():
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
