from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from database import Base

import datetime



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class ToDo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category = Column(String, index=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    priority = Column(Boolean, default=True) 
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String, nullable=True)  # e.g., 'daily', 'weekly'
    user_id = Column(Integer, ForeignKey("users.id"))
