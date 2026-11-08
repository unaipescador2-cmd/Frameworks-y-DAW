from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Se importa 'models' aunque no se use directamente: al importarlo, SQLAlchemy
# conoce las tablas y create_all puede crearlas. (El aviso de "import sin usar"
# del editor es normal.)
from app import models
from app.database import Base, engine
from app.middleware import add_process_time_header, unhandled_exception_handler
from app.routers import categories, projects, tasks

# Crea las tablas en taskflow.db si todavía no existen. Debe ir ANTES de crear la app.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Tareas y Proyectos",
    description="Práctica 1.6 - CRUD completo",
)

# Handler global: cualquier excepción no controlada devuelve {"error": "..."} con 500.
app.add_exception_handler(Exception, unhandled_exception_handler)

# Middleware propio: añade la cabecera X-Process-Time (ms) a todas las respuestas.
app.middleware("http")(add_process_time_header)

# CORS: permite que el frontend en http://localhost:5173 llame a la API.
# Se registra el último para que sea la capa más externa.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Registro de los routers: cada uno aporta las rutas de su recurso.
app.include_router(tasks.router)
app.include_router(projects.router)
app.include_router(categories.router)