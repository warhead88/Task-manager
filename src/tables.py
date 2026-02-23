from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    completed = Column(Integer, nullable=False, default=0)
    deleted = Column(Integer, nullable=False, default=0)
    timezone = Column(Integer, default=0)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String, nullable=False)
    remind_at = Column(DateTime, nullable=True)
    recurrence = Column(String, default="none")
