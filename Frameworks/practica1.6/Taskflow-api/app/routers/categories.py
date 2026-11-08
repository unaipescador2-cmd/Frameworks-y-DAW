from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

# Router de categorías: rutas bajo /categories, agrupadas como "categories" en Swagger.
router = APIRouter(prefix="/categories", tags=["categories"])


def check_name_free(name: str, db: Session, category_id: int | None = None) -> None:
    """Función auxiliar: comprueba que no exista otra categoría con el mismo nombre.

    En el modelo, 'name' es unique=True. Si intentáramos guardar un duplicado,
    la base de datos daría un error interno (500). Comprobándolo antes devolvemos
    un 409 con un mensaje claro.

    category_id sirve para el PUT: al editar una categoría, su propio nombre
    actual no cuenta como duplicado.
    """
    existing = db.query(models.Category).filter(models.Category.name == name).first()
    if existing is not None and existing.id != category_id:
        raise HTTPException(status_code=409, detail="Ya existe una categoría con ese nombre")


@router.get("", response_model=list[schemas.CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    """GET /categories -> lista todas las categorías (sin sus tareas)."""
    return db.query(models.Category).order_by(models.Category.id).all()


@router.get("/{category_id}", response_model=schemas.CategoryDetail)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """GET /categories/{id} -> detalle de la categoría CON sus tareas.

    Las tareas salen por la relación Category.tasks del modelo.
    """
    category = db.get(models.Category, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="La categoría no existe")
    return category


@router.post("", response_model=schemas.CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(data: schemas.CategoryIn, db: Session = Depends(get_db)):
    """POST /categories -> crea una categoría. Devuelve 201 (Created)."""
    check_name_free(data.name, db)                     # evita nombres duplicados
    category = models.Category(**data.model_dump())    # schema -> objeto del modelo
    db.add(category)
    db.commit()
    db.refresh(category)                               # obtiene el id generado
    return category


@router.put("/{category_id}", response_model=schemas.CategoryOut)
def update_category(category_id: int, data: schemas.CategoryIn, db: Session = Depends(get_db)):
    """PUT /categories/{id} -> edita el nombre de una categoría."""
    category = db.get(models.Category, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="La categoría no existe")
    # Se pasa category_id para que su propio nombre no cuente como duplicado.
    check_name_free(data.name, db, category_id)
    category.name = data.name
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """DELETE /categories/{id} -> elimina una categoría.

    Decisión: BLOQUEO, igual que en proyectos. Si la categoría tiene tareas
    no se elimina (409), para no borrar ni dejar huérfanas tareas del usuario
    sin que lo decida él.
    """
    category = db.get(models.Category, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="La categoría no existe")
    # category.tasks es la lista de tareas de la categoría (relación 1-N).
    if category.tasks:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar la categoría: tiene tareas asociadas. "
                   "Elimina o reasigna antes sus tareas.",
        )
    db.delete(category)
    db.commit()