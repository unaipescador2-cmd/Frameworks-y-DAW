from fastapi import FastAPI
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class VersionResponse(BaseModel):
    version: str


class PingResponse(BaseModel):
    message: str


app = FastAPI(
    title="API Práctica 1.1",
    description="API inicial desarrollada con FastAPI.",
    version="1.0.0"
)


@app.get(
    "/health",
    summary="Comprobar el estado de la API",
    description="Devuelve el estado actual del servidor.",
    response_model=HealthResponse
)
def health():
    return {"status": "ok"}


@app.get(
    "/version",
    summary="Consultar la versión de la API",
    description="Devuelve la versión actual de la API.",
    response_model=VersionResponse
)
def version():
    return {"version": "1.0.0"}


@app.get(
    "/ping",
    summary="Comprobar conectividad",
    description="Comprueba que el servidor responde correctamente.",
    response_model=PingResponse
)
def ping():
    return {"message": "pong"}