from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from contextlib import contextmanager

from tables import Base
from config import Config

engine = create_engine(Config.DATABASE_URL, echo=Config.DEBUG)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
