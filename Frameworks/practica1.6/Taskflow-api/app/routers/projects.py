from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

# Router de proyectos: rutas bajo /projects, agrupadas como "projects" en Swagger.
router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    """GET /projects -> lista todos los proyectos (sin sus tareas)."""
    return db.query(models.Project).order_by(models.Project.id).all()


@router.get("/{project_id}", response_model=schemas.ProjectDetail)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """GET /projects/{id} -> detalle del proyecto CON sus tareas.

    Las tareas salen porque el modelo tiene la relación Project.tasks y el
    schema ProjectDetail declara el campo 'tasks'.
    """
    project = db.get(models.Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="El proyecto no existe")
    return project


@router.post("", response_model=schemas.ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(data: schemas.ProjectIn, db: Session = Depends(get_db)):
    """POST /projects -> crea un proyecto. Devuelve 201 (Created)."""
    project = models.Project(**data.model_dump())   # schema -> objeto del modelo
    db.add(project)
    db.commit()
    db.refresh(project)                             # obtiene el id generado
    return project


@router.put("/{project_id}", response_model=schemas.ProjectOut)
def update_project(project_id: int, data: schemas.ProjectIn, db: Session = Depends(get_db)):
    """PUT /projects/{id} -> edita un proyecto existente."""
    project = db.get(models.Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="El proyecto no existe")
    for field, value in data.model_dump().items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """DELETE /projects/{id} -> elimina un proyecto.

    Decisión: BLOQUEO. Si el proyecto tiene tareas no se elimina (409).

    Justificación: borrar en cascada destruiría tareas del usuario sin que sea
    consciente, y una tarea no puede existir sin proyecto (project_id no admite
    NULL). Con el bloqueo, el usuario decide antes qué hacer con sus tareas.
    """
    project = db.get(models.Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="El proyecto no existe")
    if project.tasks:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el proyecto: tiene tareas asociadas. "
                   "Elimina o reasigna antes sus tareas.",
        )
    db.delete(project)
    db.commit()