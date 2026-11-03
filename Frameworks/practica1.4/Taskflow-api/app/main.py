from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middleware import add_process_time_header, unhandled_exception_handler
from app.routers import projects, tasks

app = FastAPI(
    title="API de Tareas y Proyectos",
    description="Práctica 1.4 - Middleware",
)

# Handler global: cualquier excepción no controlada devuelve {"error": "..."} con 500.
app.add_exception_handler(Exception, unhandled_exception_handler)

# Middleware propio: añade la cabecera X-Process-Time a todas las respuestas.
app.middleware("http")(add_process_time_header)

# CORS: permite que el frontend en http://localhost:5173 llame a la API.
# Se registra el último para que sea la capa más externa.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(tasks.router)
app.include_router(projects.router)