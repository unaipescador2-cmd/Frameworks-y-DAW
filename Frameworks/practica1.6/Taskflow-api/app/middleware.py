import time

from fastapi import Request
from fastapi.responses import JSONResponse

    
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler global de excepciones no controladas.

    Problema que resuelve: si un endpoint falla de forma inesperada, el cliente
    podría recibir detalles internos (stacktrace). Este handler devuelve
    siempre un mensaje genérico con código 500 y nunca expone el stacktrace.
    """
    return JSONResponse(
        status_code=500,
        content={"error": "Error interno del servidor"},
    )


async def add_process_time_header(request: Request, call_next):
    """
    Middleware que mide el tiempo de respuesta y lo añade a la cabecera
    X-Process-Time, en milisegundos.

    Problema que resuelve: permite saber cuánto tarda cada petición sin
    modificar ningún endpoint, porque se ejecuta en todas las respuestas.
    """
    start = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception as exc:
        # Si el endpoint falla, generamos aquí la respuesta 500 para que
        # también lleve X-Process-Time (el criterio pide que esté en toda respuesta).
        response = await unhandled_exception_handler(request, exc)
    elapsed_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time"] = f"{elapsed_ms:.2f}"
    return response