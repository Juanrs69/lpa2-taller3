"""
Router para endpoints de canciones.
Maneja CRUD completo de canciones: crear, leer, actualizar, eliminar, buscar.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, and_, select

from ..database import get_session
from ..models import Cancion, CancionCreate, CancionRead, CancionUpdate

router = APIRouter()


@router.get("/", response_model=list[CancionRead])
def listar_canciones(
    *, session: Session = Depends(get_session), skip: int = 0, limit: int = 100
):
    """
    Listar todas las canciones con paginación.

    - **skip**: número de registros a saltar (para paginación)
    - **limit**: máximo número de registros a retornar (máximo 100)
    """
    # Validar parámetros de paginación
    if limit > 100:
        limit = 100

    canciones = session.exec(select(Cancion).offset(skip).limit(limit)).all()

    return canciones


@router.post("/", response_model=CancionRead, status_code=status.HTTP_201_CREATED)
def crear_cancion(*, session: Session = Depends(get_session), cancion: CancionCreate):
    """
    Crear una nueva canción.

    - **titulo**: título de la canción (requerido)
    - **artista**: nombre del artista (requerido)
    - **album**: nombre del álbum (requerido)
    - **duracion**: duración en segundos (requerido)
    - **año**: año de lanzamiento (requerido)
    - **genero**: género musical (requerido)
    """
    db_cancion = Cancion.model_validate(cancion)
    session.add(db_cancion)
    session.commit()
    session.refresh(db_cancion)
    return db_cancion


@router.get("/buscar", response_model=list[CancionRead])
def buscar_canciones(
    *,
    session: Session = Depends(get_session),
    titulo: str | None = Query(None, description="Buscar por título"),
    artista: str | None = Query(None, description="Buscar por artista"),
    genero: str | None = Query(None, description="Buscar por género"),
    año: int | None = Query(None, description="Buscar por año"),
    skip: int = 0,
    limit: int = 100,
):
    """
    Buscar canciones por diferentes criterios.

    Puede buscar por título, artista, género y/o año.
    La búsqueda en texto es parcial (case-insensitive).
    """
    # Validar parámetros de paginación
    if limit > 100:
        limit = 100

    # Construir query base
    query = select(Cancion)

    # Aplicar filtros dinámicamente
    conditions = []

    if titulo:
        conditions.append(Cancion.titulo.ilike(f"%{titulo}%"))  # type: ignore

    if artista:
        conditions.append(Cancion.artista.ilike(f"%{artista}%"))  # type: ignore

    if genero:
        conditions.append(Cancion.genero.ilike(f"%{genero}%"))  # type: ignore

    if año:
        conditions.append(Cancion.año == año)

    # Aplicar filtros con AND
    if conditions:
        query = query.where(and_(*conditions))

    # Aplicar paginación
    query = query.offset(skip).limit(limit)

    canciones = session.exec(query).all()
    return canciones


@router.get("/{cancion_id}", response_model=CancionRead)
def obtener_cancion(*, session: Session = Depends(get_session), cancion_id: int):
    """
    Obtener una canción por su ID.
    """
    cancion = session.get(Cancion, cancion_id)
    if not cancion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Canción no encontrada"
        )
    return cancion


@router.put("/{cancion_id}", response_model=CancionRead)
def actualizar_cancion(
    *,
    session: Session = Depends(get_session),
    cancion_id: int,
    cancion_update: CancionUpdate,
):
    """
    Actualizar una canción existente.

    Solo se actualizarán los campos proporcionados.
    """
    cancion = session.get(Cancion, cancion_id)
    if not cancion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Canción no encontrada"
        )

    # Actualizar solo los campos proporcionados
    cancion_data = cancion_update.model_dump(exclude_unset=True)

    for field, value in cancion_data.items():
        setattr(cancion, field, value)

    session.add(cancion)
    session.commit()
    session.refresh(cancion)
    return cancion


@router.delete("/{cancion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cancion(*, session: Session = Depends(get_session), cancion_id: int):
    """
    Eliminar una canción.

    También eliminará todos los favoritos asociados a esta canción.
    """
    cancion = session.get(Cancion, cancion_id)
    if not cancion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Canción no encontrada"
        )

    session.delete(cancion)
    session.commit()
