"""
Modelos de datos de la aplicación usando SQLModel.
Define las entidades Usuario, Cancion y Favorito con validaciones Pydantic.
"""

from datetime import datetime

from pydantic import EmailStr, field_validator
from sqlmodel import Field, Relationship, SQLModel


class UsuarioBase(SQLModel):
    """Modelo base para Usuario con campos comunes."""

    nombre: str = Field(min_length=2, max_length=100, description="Nombre del usuario")
    correo: EmailStr = Field(
        unique=True, description="Correo electrónico único del usuario"
    )


class Usuario(UsuarioBase, table=True):
    """Modelo de tabla Usuario en la base de datos."""

    id: int | None = Field(default=None, primary_key=True)
    fecha_registro: datetime = Field(
        default_factory=datetime.utcnow, description="Fecha de registro del usuario"
    )

    # Relación con favoritos
    favoritos: list["Favorito"] = Relationship(back_populates="usuario")


class UsuarioCreate(UsuarioBase):
    """Modelo para crear un nuevo usuario."""

    pass


class UsuarioRead(UsuarioBase):
    """Modelo para leer datos de usuario."""

    id: int
    fecha_registro: datetime


class UsuarioUpdate(SQLModel):
    """Modelo para actualizar un usuario."""

    nombre: str | None = Field(default=None, min_length=2, max_length=100)
    correo: EmailStr | None = Field(default=None)


class CancionBase(SQLModel):
    """Modelo base para Cancion con campos comunes."""

    titulo: str = Field(
        min_length=1, max_length=200, description="Título de la canción"
    )
    artista: str = Field(
        min_length=1, max_length=100, description="Artista de la canción"
    )
    album: str = Field(min_length=1, max_length=200, description="Álbum de la canción")
    duracion: int = Field(
        gt=0, lt=3600, description="Duración en segundos (máximo 1 hora)"
    )
    año: int = Field(ge=1900, le=2100, description="Año de lanzamiento")
    genero: str = Field(min_length=1, max_length=50, description="Género musical")

    @field_validator("año")
    @classmethod
    def validar_año_no_futuro(cls, v):
        """Valida que el año no sea futuro."""
        año_actual = datetime.now().year
        if v > año_actual:
            raise ValueError(f"El año no puede ser futuro. Año actual: {año_actual}")
        return v


class Cancion(CancionBase, table=True):
    """Modelo de tabla Cancion en la base de datos."""

    id: int | None = Field(default=None, primary_key=True)
    fecha_creacion: datetime = Field(
        default_factory=datetime.utcnow, description="Fecha de creación del registro"
    )

    # Relación con favoritos
    favoritos: list["Favorito"] = Relationship(back_populates="cancion")


class CancionCreate(CancionBase):
    """Modelo para crear una nueva canción."""

    pass


class CancionRead(CancionBase):
    """Modelo para leer datos de canción."""

    id: int
    fecha_creacion: datetime


class CancionUpdate(SQLModel):
    """Modelo para actualizar una canción."""

    titulo: str | None = Field(default=None, min_length=1, max_length=200)
    artista: str | None = Field(default=None, min_length=1, max_length=100)
    album: str | None = Field(default=None, min_length=1, max_length=200)
    duracion: int | None = Field(default=None, gt=0, lt=3600)
    año: int | None = Field(default=None, ge=1900, le=2100)
    genero: str | None = Field(default=None, min_length=1, max_length=50)

    @field_validator("año")
    @classmethod
    def validar_año_no_futuro(cls, v):
        """Valida que el año no sea futuro."""
        if v is not None:
            año_actual = datetime.now().year
            if v > año_actual:
                raise ValueError(
                    f"El año no puede ser futuro. Año actual: {año_actual}"
                )
        return v


class FavoritoBase(SQLModel):
    """Modelo base para Favorito con campos comunes."""

    id_usuario: int = Field(foreign_key="usuario.id", description="ID del usuario")
    id_cancion: int = Field(foreign_key="cancion.id", description="ID de la canción")


class Favorito(FavoritoBase, table=True):
    """Modelo de tabla Favorito en la base de datos."""

    id: int | None = Field(default=None, primary_key=True)
    fecha_marcado: datetime = Field(
        default_factory=datetime.utcnow,
        description="Fecha en que se marcó como favorito",
    )

    # Relaciones
    usuario: Usuario | None = Relationship(back_populates="favoritos")
    cancion: Cancion | None = Relationship(back_populates="favoritos")


class FavoritoCreate(FavoritoBase):
    """Modelo para crear un nuevo favorito."""

    pass


class FavoritoRead(FavoritoBase):
    """Modelo para leer datos de favorito."""

    id: int
    fecha_marcado: datetime
    # Incluir datos anidados cuando sea necesario
    usuario: UsuarioRead | None = None
    cancion: CancionRead | None = None


class FavoritoReadSimple(FavoritoBase):
    """Modelo simple para leer datos de favorito sin relaciones anidadas."""

    id: int
    fecha_marcado: datetime


# Modelos de respuesta con datos relacionados
class UsuarioConFavoritos(UsuarioRead):
    """Modelo para usuario con sus canciones favoritas."""

    favoritos: list[FavoritoReadSimple] = []


class CancionConFavoritos(CancionRead):
    """Modelo para canción con información de favoritos."""

    favoritos: list[FavoritoReadSimple] = []


# Modelo para búsqueda de canciones
class BusquedaCancion(SQLModel):
    """Modelo para parámetros de búsqueda de canciones."""

    titulo: str | None = Field(default=None, description="Buscar por título")
    artista: str | None = Field(default=None, description="Buscar por artista")
    genero: str | None = Field(default=None, description="Buscar por género")
    año: int | None = Field(default=None, description="Buscar por año")


# Actualizar referencias forward de SQLModel
UsuarioRead.model_rebuild()
CancionRead.model_rebuild()
FavoritoRead.model_rebuild()
UsuarioConFavoritos.model_rebuild()
CancionConFavoritos.model_rebuild()
