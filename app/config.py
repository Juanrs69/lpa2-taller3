"""
Configuración de la aplicación.
Maneja diferentes entornos: desarrollo, pruebas y producción.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuración de la aplicación usando Pydantic Settings.
    Lee las variables de entorno desde el archivo .env
    """

    # Configuración básica de la aplicación
    app_name: str = "API de Música"
    app_version: str = "1.0.0"
    description: str = "Una API RESTful para gestionar usuarios, canciones y favoritos"

    # Configuración del entorno
    environment: str = "development"

    # Configuración de la base de datos
    # Para SQLite: sqlite:///./musica.db
    # Para PostgreSQL: postgresql://user:password@localhost/dbname
    database_url: str = "sqlite:///./musica.db"

    # Configuración del servidor
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = True

    # Configuración de CORS
    # En desarrollo puedes usar ["*"], en producción especifica los orígenes permitidos
    cors_origins: list[str] = ["*"]

    # Configuración de seguridad
    secret_key: str = "mi_clave_secreta_super_segura_123"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Configuración de logging
    log_level: str = "INFO"

    class Config:
        """
        Configuración de Pydantic Settings.
        """

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Crear una instancia global de Settings
settings = Settings()


# Crear diferentes configuraciones para cada entorno
class DevelopmentSettings(Settings):
    """Configuración para el entorno de desarrollo."""

    debug: bool = True


class TestingSettings(Settings):
    """Configuración para el entorno de pruebas."""

    # Usar una base de datos diferente para pruebas
    database_url: str = "sqlite:///./test_musica.db"
    debug: bool = True


class ProductionSettings(Settings):
    """Configuración para el entorno de producción."""

    debug: bool = False
    cors_origins: list[str] = ["https://mi-dominio.com"]


# Función para obtener la configuración según el entorno
def get_settings() -> Settings:
    """
    Retorna la configuración apropiada según el entorno.
    """
    env = settings.environment.lower()

    if env == "testing":
        return TestingSettings()
    elif env == "production":
        return ProductionSettings()
    else:
        return DevelopmentSettings()
