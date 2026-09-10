from uuid import uuid4
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


class Task(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreate(BaseModel):
    title: str

tasks: list[Task] = []

class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

class BookCreate(BaseModel):
    book: str
book: str = ""


@app.get("/tasks", response_model=list[Task])
def read_tasks() -> list[Task]:
    return tasks

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload:TaskCreate) -> Task:
    task = Task(
        id=str(uuid4()),
        title=payload.title,
        completed=False
    )
    tasks.append(task)
    return task

@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, payload: TaskUpdate) -> Task:
    for task in tasks:
        if task.id == task_id:
            if payload.title is not None:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str) -> None:
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")


@app.get("/book",)
def get_book() -> str:
    if not book:
        return "А нет любимой книги!"
    return f"Любимая книга: {book}"

@app.post("/book", status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate):
    global book
    book = payload.book
    return book

