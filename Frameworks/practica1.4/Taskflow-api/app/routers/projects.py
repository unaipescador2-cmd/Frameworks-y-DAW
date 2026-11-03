from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/projects", tags=["projects"])


class Project(BaseModel):
    id: int
    name: str
    description: str | None = None


# Base de datos en memoria (de ejemplo)
projects_db: list[Project] = [
    Project(id=1, name="Proyecto API", description="API de tareas con FastAPI"),
]


@router.get("/", response_model=list[Project])
def list_projects():
    return projects_db


@router.get("/{project_id}", response_model=Project)
def get_project(project_id: int):
    for project in projects_db:
        if project.id == project_id:
            return project
    raise HTTPException(status_code=404, detail="Proyecto no encontrado")


@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(project: Project):
    projects_db.append(project)
    return project


@router.put("/{project_id}", response_model=Project)
def update_project(project_id: int, updated: Project):
    for index, project in enumerate(projects_db):
        if project.id == project_id:
            projects_db[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Proyecto no encontrado")


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int):
    for index, project in enumerate(projects_db):
        if project.id == project_id:
            projects_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Proyecto no encontrado")