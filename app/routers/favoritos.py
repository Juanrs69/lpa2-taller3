"""
Router para endpoints de favoritos.
Maneja la gestión de canciones favoritas de usuarios.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, and_, select

from ..database import get_session
from ..models import Cancion, Favorito, FavoritoCreate, FavoritoRead, Usuario

router = APIRouter()


@router.get("/", response_model=list[FavoritoRead])
def listar_favoritos(
    *, session: Session = Depends(get_session), skip: int = 0, limit: int = 100
):
    """
    Listar todos los favoritos con paginación.

    - **skip**: número de registros a saltar (para paginación)
    - **limit**: máximo número de registros a retornar (máximo 100)
    """
    # Validar parámetros de paginación
    if limit > 100:
        limit = 100

    favoritos = session.exec(select(Favorito).offset(skip).limit(limit)).all()

    return favoritos


@router.post("/", response_model=FavoritoRead, status_code=status.HTTP_201_CREATED)
def crear_favorito(
    *, session: Session = Depends(get_session), favorito: FavoritoCreate
):
    """
    Marcar una canción como favorita para un usuario.

    - **id_usuario**: ID del usuario (requerido)
    - **id_cancion**: ID de la canción (requerido)
    """
    # Verificar que el usuario existe
    usuario = session.get(Usuario, favorito.id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    # Verificar que la canción existe
    cancion = session.get(Cancion, favorito.id_cancion)
    if not cancion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Canción no encontrada"
        )

    # Verificar que no existe ya este favorito
    favorito_existente = session.exec(
        select(Favorito).where(
            and_(
                Favorito.id_usuario == favorito.id_usuario,
                Favorito.id_cancion == favorito.id_cancion,
            )
        )
    ).first()

    if favorito_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta canción ya está marcada como favorita para este usuario",
        )

    # Crear el favorito
    db_favorito = Favorito.model_validate(favorito)
    session.add(db_favorito)
    session.commit()
    session.refresh(db_favorito)
    return db_favorito


@router.get("/{favorito_id}", response_model=FavoritoRead)
def obtener_favorito(*, session: Session = Depends(get_session), favorito_id: int):
    """
    Obtener un favorito por su ID.
    """
    favorito = session.get(Favorito, favorito_id)
    if not favorito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Favorito no encontrado"
        )
    return favorito


@router.delete("/{favorito_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_favorito(*, session: Session = Depends(get_session), favorito_id: int):
    """
    Eliminar un favorito (desmarcar como favorito).
    """
    favorito = session.get(Favorito, favorito_id)
    if not favorito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Favorito no encontrado"
        )

    session.delete(favorito)
    session.commit()


@router.post(
    "/{id_usuario}/canciones/{id_cancion}",
    response_model=FavoritoRead,
    status_code=status.HTTP_201_CREATED,
)
def marcar_favorito_especifico(
    *, session: Session = Depends(get_session), id_usuario: int, id_cancion: int
):
    """
    Marcar una canción específica como favorita para un usuario específico.

    Endpoint alternativo más específico para marcar favoritos.
    """
    # Verificar que el usuario existe
    usuario = session.get(Usuario, id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    # Verificar que la canción existe
    cancion = session.get(Cancion, id_cancion)
    if not cancion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Canción no encontrada"
        )

    # Verificar que no existe ya este favorito
    favorito_existente = session.exec(
        select(Favorito).where(
            and_(Favorito.id_usuario == id_usuario, Favorito.id_cancion == id_cancion)
        )
    ).first()

    if favorito_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta canción ya está marcada como favorita para este usuario",
        )

    # Crear el favorito
    favorito_data = FavoritoCreate(id_usuario=id_usuario, id_cancion=id_cancion)
    db_favorito = Favorito.model_validate(favorito_data)
    session.add(db_favorito)
    session.commit()
    session.refresh(db_favorito)
    return db_favorito


@router.delete(
    "/{id_usuario}/canciones/{id_cancion}", status_code=status.HTTP_204_NO_CONTENT
)
def eliminar_favorito_especifico(
    *, session: Session = Depends(get_session), id_usuario: int, id_cancion: int
):
    """
    Eliminar un favorito específico (desmarcar canción favorita de un usuario).
    """
    # Buscar el favorito específico
    favorito = session.exec(
        select(Favorito).where(
            and_(Favorito.id_usuario == id_usuario, Favorito.id_cancion == id_cancion)
        )
    ).first()

    if not favorito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Favorito no encontrado"
        )

    session.delete(favorito)
    session.commit()
