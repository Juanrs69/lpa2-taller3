from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.database import check_database_connection, create_db_and_tables
from app.routers import canciones, favoritos, usuarios

# Obtener configuración
settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Gestor de ciclo de vida de la aplicación.
    Se ejecuta al iniciar y al cerrar la aplicación.
    """
    # Startup: Crear tablas en la base de datos
    create_db_and_tables()
    yield

    # Shutdown: Limpiar recursos si es necesario
    print("cerrando aplicación...")


# Crear la instancia de FastAPI con metadatos apropiados
app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.app_version,
    lifespan=lifespan,
    contact={
        "name": "Juan Alejandro Ramirez Sanchez",
        "email": "juan.ramirez@ejemplo.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)


# Configurar CORS para permitir solicitudes desde diferentes orígenes
# Esto es importante para desarrollo con frontend separado
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir los routers de usuarios, canciones y favoritos
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(canciones.router, prefix="/api/canciones", tags=["Canciones"])
app.include_router(favoritos.router, prefix="/api/favoritos", tags=["Favoritos"])

# Montar archivos estáticos para el frontend
app.mount("/static", StaticFiles(directory="static"), name="static")


# Servir el frontend en la ruta raíz
@app.get("/", tags=["Frontend"])
async def serve_frontend():
    """
    Servir la aplicación frontend en la ruta raíz.
    """
    return FileResponse("static/index.html")


# Crear un endpoint de información de la API
@app.get("/api", tags=["Root"])
async def api_info():
    """
    Endpoint con información básica de la API.
    Retorna información básica y enlaces a la documentación.
    """
    return {
        "message": f"Bienvenido a {settings.app_name}",
        "version": settings.app_version,
        "description": settings.description,
        "developer": "Juan Alejandro Ramirez Sanchez",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "usuarios": "/api/usuarios",
            "canciones": "/api/canciones",
            "favoritos": "/api/favoritos",
        },
    }


# Crear un endpoint de health check para monitoreo
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint para verificar el estado de la API.
    Útil para sistemas de monitoreo y orquestación.
    """
    # Verificar conexión a base de datos
    db_status = "connected" if check_database_connection() else "disconnected"

    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "database": db_status,
        "environment": settings.environment,
        "version": settings.app_version,
    }


# TODO: Opcional - Agregar middleware para logging de requests


# TODO: Opcional - Agregar manejadores de errores personalizados


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
