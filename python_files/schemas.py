from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class TodoBase(BaseModel):
    title: str
    category: str
    due_date: Optional[datetime] = None
    priority: bool = True
    is_recurring: Optional[bool] = False
    recurrence_pattern: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    completed: bool

class TodoResponse(TodoBase):
    id: int
    completed: bool
    completed_at: Optional[datetime]
    user_id: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
