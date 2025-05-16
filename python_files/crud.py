from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime

def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.ToDo(**todo.dict(), user_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todos(db: Session, user_id: int):
    return db.query(models.ToDo).filter(models.ToDo.user_id == user_id).all()

def update_todo(db: Session, todo_id: int, completed: bool):
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if todo:
        todo.completed = completed
        todo.completed_at = datetime.utcnow() if completed else None
        db.commit()
        db.refresh(todo)
    return todo

def get_analytics(db: Session, user_id: int):
    todos = db.query(models.ToDo).filter(models.ToDo.user_id == user_id).all()
    total = len(todos)
    completed = sum(1 for t in todos if t.completed)
    incomplete = total - completed
    overdue = sum(1 for t in todos if not t.completed and t.due_date and t.due_date < datetime.utcnow())
    
    by_category = {}
    for todo in todos:
        if todo.category not in by_category:
            by_category[todo.category] = {"completed": 0, "incomplete": 0}
        if todo.completed:
            by_category[todo.category]["completed"] += 1
        else:
            by_category[todo.category]["incomplete"] += 1

    return {
        "total": total,
        "completed": completed,
        "incomplete": incomplete,
        "overdue": overdue,
        "by_category": by_category
    }
