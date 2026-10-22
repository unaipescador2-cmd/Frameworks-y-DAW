"""Schemas Pydantic del dominio TaskFlow."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------
class ProjectCreate(BaseModel):
    """Datos que el cliente envía para crear un proyecto."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre del proyecto (entre 1 y 100 caracteres)",
        examples=["Rediseño web"],
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Descripción opcional del proyecto (máx. 500 caracteres)",
        examples=["Rediseño completo de la web corporativa"],
    )

    # Ejemplo completo que Swagger muestra en el "Example Value" del body
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Rediseño web",
                "description": "Rediseño completo de la web corporativa",
            }
        }
    )


class ProjectRead(ProjectCreate):
    """Datos que la API devuelve de un proyecto (incluye los de ProjectCreate)."""

    id: int = Field(..., description="Identificador único del proyecto")
    created_at: datetime = Field(..., description="Fecha y hora de creación")

    # from_attributes permite construir el schema desde objetos ORM (SQLAlchemy)
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Rediseño web",
                "description": "Rediseño completo de la web corporativa",
                "created_at": "2026-10-22T10:00:00",
            }
        },
    )


# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------
class TaskCreate(BaseModel):
    """Datos que el cliente envía para crear una tarea."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Título de la tarea (entre 1 y 100 caracteres)",
        examples=["Preparar la presentación"],
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Descripción opcional de la tarea (máx. 500 caracteres)",
        examples=["Incluir resultados del último sprint"],
    )
    project_id: int = Field(
        ...,
        gt=0,
        description="ID del proyecto al que pertenece la tarea (mayor que 0)",
        examples=[1],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Preparar la presentación",
                "description": "Incluir resultados del último sprint",
                "project_id": 1,
            }
        }
    )


class TaskRead(TaskCreate):
    """Datos que la API devuelve de una tarea (incluye los de TaskCreate)."""

    id: int = Field(..., description="Identificador único de la tarea")
    completed: bool = Field(default=False, description="Si la tarea está completada")
    created_at: datetime = Field(..., description="Fecha y hora de creación")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Preparar la presentación",
                "description": "Incluir resultados del último sprint",
                "project_id": 1,
                "completed": False,
                "created_at": "2026-10-22T10:00:00",
            }
        },
    )