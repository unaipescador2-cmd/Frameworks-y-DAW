from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

# Router de tareas. El prefijo hace que todas las rutas empiecen por /tasks y
# el tag las agrupa bajo "tasks" en Swagger.
router = APIRouter(prefix="/tasks", tags=["tasks"])

def check_relations(data: schemas.TaskIn, db: Session) -> None:
    """Comprueba que el proyecto y la categoría indicados existen."""
    if db.get(models.Project, data.project_id) is None:
        raise HTTPException(status_code=404, detail="El proyecto no existe")
    if data.category_id is not None and db.get(models.Category, data.category_id) is None:
        raise HTTPException(status_code=404, detail="La categoría no existe")

@router.get("", response_model=list[schemas.TaskOut])
def list_tasks(
    project_id: int | None = None,          # filtro opcional: ?project_id=1
    completed: bool | None = None,          # filtro opcional: ?completed=true
    skip: int = Query(0, ge=0),             # paginación: cuántas tareas saltar
    limit: int = Query(10, ge=1, le=100),   # paginación: cuántas devolver
    db: Session = Depends(get_db),
):
    """GET /tasks -> lista tareas con filtros opcionales y paginación."""
    query = db.query(models.Task)
    if project_id is not None:
        query = query.filter(models.Task.project_id == project_id)
    if completed is not None:
        # El parámetro se llama 'completed' (lo pide el contrato) pero la
        # columna del modelo se llama 'done'.
        query = query.filter(models.Task.done == completed)
    return query.order_by(models.Task.id).offset(skip).limit(limit).all()


@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """GET /tasks/{id} -> detalle de una tarea."""
    task = db.get(models.Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="La tarea no existe")
    return task


@router.post("", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(data: schemas.TaskIn, db: Session = Depends(get_db)):
    """POST /tasks -> crea una tarea. Devuelve 201 (Created)."""
    check_relations(data, db)
    task = models.Task(**data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, data: schemas.TaskIn, db: Session = Depends(get_db)):
    """PUT /tasks/{id} -> edita una tarea existente."""
    task = db.get(models.Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="La tarea no existe")
    check_relations(data, db)
    for field, value in data.model_dump().items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """DELETE /tasks/{id} -> elimina una tarea. Devuelve 204 (sin contenido)."""
    task = db.get(models.Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="La tarea no existe")
    db.delete(task)