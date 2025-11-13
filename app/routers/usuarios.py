"""
Router para endpoints de usuarios.
Maneja CRUD completo de usuarios: crear, leer, actualizar, eliminar.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from ..database import get_session
from ..models import (
    Usuario,
    UsuarioConFavoritos,
    UsuarioCreate,
    UsuarioRead,
    UsuarioUpdate,
)

router = APIRouter()


@router.get("/", response_model=list[UsuarioRead])
def listar_usuarios(
    *, session: Session = Depends(get_session), skip: int = 0, limit: int = 100
):
    """
    Listar todos los usuarios con paginación.

    - **skip**: número de registros a saltar (para paginación)
    - **limit**: máximo número de registros a retornar (máximo 100)
    """
    # Validar parámetros de paginación
    if limit > 100:
        limit = 100

    usuarios = session.exec(select(Usuario).offset(skip).limit(limit)).all()

    return usuarios


@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(*, session: Session = Depends(get_session), usuario: UsuarioCreate):
    """
    Crear un nuevo usuario.

    - **nombre**: nombre del usuario (requerido)
    - **correo**: correo electrónico único (requerido)
    """
    try:
        db_usuario = Usuario.model_validate(usuario)
        session.add(db_usuario)
        session.commit()
        session.refresh(db_usuario)
        return db_usuario
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado",
        ) from e


@router.get("/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(*, session: Session = Depends(get_session), usuario_id: int):
    """
    Obtener un usuario por su ID.
    """
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return usuario


@router.put("/{usuario_id}", response_model=UsuarioRead)
def actualizar_usuario(
    *,
    session: Session = Depends(get_session),
    usuario_id: int,
    usuario_update: UsuarioUpdate,
):
    """
    Actualizar un usuario existente.

    Solo se actualizarán los campos proporcionados.
    """
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    # Actualizar solo los campos proporcionados
    usuario_data = usuario_update.model_dump(exclude_unset=True)

    try:
        for field, value in usuario_data.items():
            setattr(usuario, field, value)

        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado",
        ) from e


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(*, session: Session = Depends(get_session), usuario_id: int):
    """
    Eliminar un usuario.

    También eliminará todos sus favoritos asociados.
    """
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    session.delete(usuario)
    session.commit()


@router.get("/{usuario_id}/favoritos", response_model=UsuarioConFavoritos)
def listar_favoritos_usuario(
    *, session: Session = Depends(get_session), usuario_id: int
):
    """
    Listar todas las canciones favoritas de un usuario.
    """
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    return usuario
