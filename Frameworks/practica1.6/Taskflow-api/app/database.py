from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# URL de conexión: SQLite guarda todo en un único archivo, taskflow.db,
# que se crea en la carpeta desde la que se arranca la aplicación.
SQLALCHEMY_DATABASE_URL = "sqlite:///./taskflow.db"

# Engine: punto de conexión con la base de datos.
# check_same_thread=False es necesario con SQLite y FastAPI: FastAPI puede
# atender una petición en un hilo distinto al que abrió la conexión, y SQLite
# por defecto lo prohíbe. Con False se permite compartir la conexión entre hilos.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# SessionLocal: fábrica de sesiones. Cada petición crea una sesión propia.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: clase de la que heredan todos los modelos (declarative).
Base = declarative_base()


def get_db():
    """
    Dependencia de FastAPI: proporciona una sesión de base de datos por petición.

    Con yield, la sesión se entrega al endpoint, y el bloque finally se ejecuta
    al terminar la petición (incluso si hay un error), cerrando siempre la sesión
    y evitando conexiones abiertas.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()