from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/tasks", tags=["tasks"])


class Task(BaseModel):
    id: int
    title: str
    done: bool = False


# Base de datos en memoria (de ejemplo)
tasks_db: list[Task] = [
    Task(id=1, title="Aprender FastAPI"),
    Task(id=2, title="Hacer la práctica 1.3", done=True),
]


@router.get("/", response_model=list[Task])
def list_tasks():
    return tasks_db


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: Task):
    tasks_db.append(task)
    return task


@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, updated: Task):
    for index, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for index, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Tarea no encontrada")