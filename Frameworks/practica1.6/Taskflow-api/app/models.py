from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base

# Cada clase de este archivo se mapea a una tabla de la base de datos (ORM):
# la clase es la tabla, cada atributo Column es una columna y cada objeto
# creado es una fila.


class User(Base):
    """Usuario de la aplicación. Un usuario puede tener muchas tareas (1-N)."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    tasks = relationship("Task", back_populates="user")


class Project(Base):
    """Proyecto. Un proyecto contiene muchas tareas (1-N).
    No tiene dueño: todos los usuarios pueden acceder a todos los proyectos."""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    tasks = relationship("Task", back_populates="project")


class Category(Base):
    """Categoría para clasificar tareas. Una categoría agrupa muchas tareas (1-N)."""

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    tasks = relationship("Task", back_populates="category")


class Task(Base):
    """Tarea. Pertenece obligatoriamente a un proyecto (FK project_id)."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    done = Column(Boolean, default=False)

    # Claves foráneas: enlazan cada tarea con su proyecto, categoría y usuario.
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    project = relationship("Project", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")
    user = relationship("User", back_populates="tasks")