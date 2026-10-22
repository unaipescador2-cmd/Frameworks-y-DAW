"""TaskFlow API - Práctica 1.2: modelado con Pydantic."""
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas import TaskCreate, TaskRead

app = FastAPI(
    title="TaskFlow API",
    description="API de gestión de tareas y proyectos (Práctica 1.2).",
    version="0.1.0",
)


# ---------------------------------------------------------------------------
# Errores de validación (422) con formato claro y consistente
# ---------------------------------------------------------------------------
def _mensaje_legible(error: dict) -> str:
    """Traduce un error de Pydantic a un mensaje en castellano."""
    tipo = error["type"]
    ctx = error.get("ctx", {})

    if tipo == "string_too_short":
        return f"No puede tener menos de {ctx.get('min_length')} carácter(es); no puede estar vacío."
    if tipo == "string_too_long":
        return f"No puede superar los {ctx.get('max_length')} caracteres."
    if tipo == "missing":
        return "Este campo es obligatorio."
    if tipo == "greater_than":
        return f"Debe ser mayor que {ctx.get('gt')}."
    if tipo in ("int_parsing", "int_type"):
        return "Debe ser un número entero."
    if tipo in ("string_type",):
        return "Debe ser un texto."
    return error["msg"]  # mensaje por defecto de Pydantic


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Devuelve el 422 con un detalle legible: campo, mensaje y valor recibido."""
    detalles = [
        {
            "campo": ".".join(str(p) for p in err["loc"] if p != "body"),
            "mensaje": _mensaje_legible(err),
            "valor_recibido": err.get("input"),
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"error": "Error de validación", "detalle": detalles},
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.post(
    "/tasks",
    response_model=TaskRead,
    status_code=201,
    summary="Crear una tarea (temporal)",
    tags=["tasks"],
)
def create_task(task: TaskCreate) -> TaskRead:
    """Endpoint temporal: no guarda nada, devuelve un `TaskRead` simulado.

    Ejemplo de uso:

    ```json
    {"title": "Preparar la presentación", "project_id": 1}
    ```

    Si `title` está vacío o supera los 100 caracteres, la API responde con
    **422 Unprocessable Entity** y el detalle del error.
    """
    return TaskRead(
        id=1,  # ID simulado (aún no hay base de datos)
        completed=False,
        created_at=datetime.now(),
        **task.model_dump(),
    )