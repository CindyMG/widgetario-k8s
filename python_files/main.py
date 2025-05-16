from fastapi import FastAPI, Request, Depends, Form, HTTPException, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import crud, models, schemas
from database import SessionLocal, engine
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import status
from datetime import datetime, timedelta
from models import ToDo
from starlette_exporter import PrometheusMiddleware, handle_metrics
import os
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import metrics



app = FastAPI()
templates = Jinja2Templates(directory="templates")

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Example custom counter for tasks created
task_create_counter = Counter("tasks_created_total", "Total number of tasks created")

@app.post("/tasks")
async def create_task():
    task_create_counter.inc()
    return {"message": "Task created"}

# JWT settings
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database setup
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Redirect to login")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Redirect to login")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Redirect to login")

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Redirect to login")
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        return None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# ------------------- ROUTES -------------------
app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    username = decode_token(token)
    if not username:
        return RedirectResponse("/", status_code=302)

    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return RedirectResponse("/", status_code=302)

    todos = crud.get_todos(db, user.id)
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

# Login form
@app.get("/", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

# Login logic
@app.post("/login")
def login(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

    token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    response = RedirectResponse("/dashboard", status_code=302)
    response.set_cookie(key="token", value=token, httponly=True)
    return response

# Register form
@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "error": None})

# Register logic
@app.post("/register")
def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Username already exists"})

    hashed_password = get_password_hash(password)
    new_user = models.User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return RedirectResponse("/", status_code=302)

# Dashboard / To-Do list
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    if not token:
        return RedirectResponse("/", status_code=302)
    
    username = decode_token(token)
    if not username:
        return RedirectResponse("/", status_code=302)

    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return RedirectResponse("/", status_code=302)

    todos = crud.get_todos(db, user.id)
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos, "username": username})

@app.get("/create", response_class=HTMLResponse)
def create(request: Request):
    return templates.TemplateResponse("create.html", {"request": request, "error": None})

# Create To-Do
@app.post("/create")
def create_todo(
    request: Request,
    title: str = Form(...),
    category: str = Form(...),
    due_date: str = Form(...),     # e.g. "2025-05-14"
    due_time: str = Form(...),     # e.g. "14:30"
    priority: str = Form(...),
    db: Session = Depends(get_db)
):
    token = request.cookies.get("token")
    username = decode_token(token)
    if not username:
        return RedirectResponse("/dashboard", status_code=302)

    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return RedirectResponse("/", status_code=302)

    # Combine date and time to create full datetime
    combined_datetime_str = f"{due_date}T{due_time}"
    due_datetime = datetime.fromisoformat(combined_datetime_str)

    todo_data = schemas.TodoCreate(
        title=title,
        category=category,
        due_date=due_datetime,
        priority=priority
    )

    crud.create_todo(db=db, todo=todo_data, user_id=user.id)
    return RedirectResponse("/dashboard", status_code=302)

# Complete a task
@app.get("/complete/{todo_id}")
def complete_todo(todo_id: int, request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    username = decode_token(token)
    if not username:
        return RedirectResponse("/", status_code=302)

    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return RedirectResponse("/", status_code=302)

    crud.update_todo(db, todo_id, completed=True)
    return RedirectResponse("/dashboard", status_code=302)

@app.get("/analytics", response_class=HTMLResponse)
def analytics(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)  # Get currently logged-in user
    todos = crud.get_todos(db, user.id)

    total = len(todos)
    completed = len([t for t in todos if t.completed])
    incomplete = total - completed
    overdue = len([t for t in todos if t.due_date and not t.completed and t.due_date < datetime.utcnow()])

    # Category-wise stats
    by_category = {}
    for t in todos:
        cat = t.category or "Uncategorized"
        if cat not in by_category:
            by_category[cat] = {"completed": 0, "incomplete": 0}
        if t.completed:
            by_category[cat]["completed"] += 1
        else:
            by_category[cat]["incomplete"] += 1

    # Completion rate
    completion_rate = round((completed / total) * 100, 2) if total > 0 else 0

    # Task streaks (assumes completed_at is filled correctly)
    completed_dates = sorted(set([t.completed_at.date() for t in todos if t.completed and t.completed_at]))
    current_streak = 0
    longest_streak = 0
    if completed_dates:
        streak = 1
        for i in range(1, len(completed_dates)):
            if completed_dates[i] == completed_dates[i - 1] + timedelta(days=1):
                streak += 1
            else:
                longest_streak = max(longest_streak, streak)
                streak = 1
        longest_streak = max(longest_streak, streak)

        # Check for current streak
        today = datetime.utcnow().date()
        if completed_dates[-1] == today:
            current_streak = 1
            for i in range(len(completed_dates) - 2, -1, -1):
                if completed_dates[i] == today - timedelta(days=current_streak):
                    current_streak += 1
                else:
                    break

    return templates.TemplateResponse("analytics.html", {
        "request": request,
        "total": total,
        "completed": completed,
        "incomplete": incomplete,
        "overdue": overdue,
        "by_category": by_category,
        "completion_rate": completion_rate,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
    })

# Logout
@app.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("token")
    return response

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    # Optional: check DB connection here
    return {"status": "ready"}


