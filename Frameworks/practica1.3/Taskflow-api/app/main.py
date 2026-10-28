from fastapi import FastAPI

from app.routers import projects, tasks

tags_metadata = [
    {"name": "tasks", "description": "Operaciones sobre las tareas."},
    {"name": "projects", "description": "Operaciones sobre los proyectos."},
]

app = FastAPI(
    title="API de Tareas y Proyectos",
    description="Práctica 1.3 - Organización con APIRouter",
    openapi_tags=tags_metadata,
)

app.include_router(tasks.router)
app.include_router(projects.router)