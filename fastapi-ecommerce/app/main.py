from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "Taskflow API"),
    version=os.getenv("APP_VERSION", "1.0.0")
)


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=5, max_length=500)
    priority: int = Field(ge=1, le=5)


class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=100)
    description: str | None = Field(None, min_length=5, max_length=500)
    priority: int | None = Field(None, ge=1, le=5)
    completed: bool | None = None


tasks = []


@app.get('/')
def home():
    return {"message": "Welcome to TaskFlow API"}


@app.get('/health')
def get_health():
    return {"status": "healthy"}


@app.get('/tasks')
def get_tasks():
    return tasks


@app.get('/tasks/{task_id}')
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(404, "Task Not Found")


@app.post('/tasks')
def create_task(task: TaskCreate):
    new_task = {
        "id": len(tasks)+1,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "completed": False
    }
    tasks.append(new_task)
    return new_task


@app.put('/tasks/{task_id}')
def update_task(task_id: int, data: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            task.update(data.model_dump(exclude_unset=True))
            return task
    raise HTTPException(404,"Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id:int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            return tasks.pop(i)

    raise HTTPException(404,"Task not found")