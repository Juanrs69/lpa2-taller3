"""
Configuración y manejo de la base de datos.
Maneja la conexión a SQLite/PostgreSQL usando SQLModel y SQLAlchemy.
"""

from collections.abc import Generator

from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

from .config import get_settings

# Obtener configuración
settings = get_settings()

# Crear el engine de la base de datos
# Para SQLite: connect_args={"check_same_thread": False} permite múltiples hilos
# Para PostgreSQL, esto no es necesario
connect_args = (
    {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)

engine: Engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    echo=settings.debug,  # Mostrar SQL queries en debug mode
)


def create_db_and_tables():
    """
    Crear todas las tablas en la base de datos.
    Se ejecuta al inicio de la aplicación.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency para obtener una sesión de base de datos.
    Se usa como dependencia en los endpoints de FastAPI.

    Yields:
        Session: Sesión de base de datos SQLModel
    """
    with Session(engine) as session:
        yield session


def get_test_session() -> Generator[Session, None, None]:
    """
    Sesión especial para testing.
    Crea un engine en memoria para pruebas.
    """
    from sqlmodel import create_engine
    from sqlmodel.pool import StaticPool

    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session


# Función de utilidad para verificar la conexión
def check_database_connection() -> bool:
    """
    Verifica si la conexión a la base de datos está funcionando.

    Returns:
        bool: True si la conexión es exitosa, False en caso contrario
    """
    try:
        from sqlalchemy import text

        with Session(engine) as session:
            # Ejecutar una query simple para verificar la conexión
            session.exec(text("SELECT 1")).first()  # type: ignore
            return True
    except Exception as e:
        print(f"Error de conexión a la base de datos: {e}")
        return False


# Función para limpiar la base de datos (útil para testing)
def clear_database():
    """
    Elimina todos los datos de las tablas.
    ¡CUIDADO! Solo usar en testing o desarrollo.
    """
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
