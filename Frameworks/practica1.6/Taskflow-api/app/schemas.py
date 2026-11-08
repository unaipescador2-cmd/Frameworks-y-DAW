from pydantic import BaseModel, ConfigDict

# Schemas Pydantic: validan los datos que entran y salen por la API.
# Son distintos de los modelos de models.py, que representan las tablas.


class TaskIn(BaseModel):
    """Datos que se envían para crear o editar una tarea."""
    title: str
    description: str | None = None
    done: bool = False
    project_id: int
    category_id: int | None = None


class TaskOut(TaskIn):
    """Tarea tal como la devuelve la API (incluye el id)."""
    id: int
    model_config = ConfigDict(from_attributes=True)


class ProjectIn(BaseModel):
    name: str
    description: str | None = None


class ProjectOut(ProjectIn):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ProjectDetail(ProjectOut):
    """Proyecto con sus tareas asociadas (para GET /projects/{id})."""
    tasks: list[TaskOut] = []


class CategoryIn(BaseModel):
    name: str


class CategoryOut(CategoryIn):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CategoryDetail(CategoryOut):
    """Categoría con sus tareas asociadas (para GET /categories/{id})."""
    tasks: list[TaskOut] = []