import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.future import select

from src.tables import Base, User, Task

# Fixture to create an in-memory SQLite database for testing
@pytest_asyncio.fixture
async def async_session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    
    async with SessionLocal() as session:
        yield session
        
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
    await engine.dispose()

@pytest.mark.asyncio
async def test_create_user(async_session: AsyncSession):
    user = User(id=123, completed=0, deleted=0, timezone=3)
    async_session.add(user)
    await async_session.commit()
    
    result = await async_session.execute(select(User).filter_by(id=123))
    db_user = result.scalars().first()
    
    assert db_user is not None
    assert db_user.id == 123
    assert db_user.timezone == 3

@pytest.mark.asyncio
async def test_create_task_and_reminders(async_session: AsyncSession):
    user = User(id=999, completed=0, deleted=0)
    async_session.add(user)
    
    task = Task(user_id=999, description="Write tests", recurrence="daily")
    async_session.add(task)
    await async_session.commit()
    
    result = await async_session.execute(select(Task).filter_by(user_id=999))
    db_tasks = result.scalars().all()
    
    assert len(db_tasks) == 1
    assert db_tasks[0].description == "Write tests"
    assert db_tasks[0].recurrence == "daily"
    assert db_tasks[0].remind_at is None
