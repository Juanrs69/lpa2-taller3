"""
Tests para la API de Música.
Pruebas unitarias y de integración usando pytest.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database import get_session
from app.models import Cancion, Favorito, Usuario
from main import app

# =============================================================================
# CONFIGURACIÓN DE FIXTURES
# =============================================================================


# Fixture para crear una base de datos en memoria para testing
@pytest.fixture(name="session")
def session_fixture():
    """
    Crea una sesión de base de datos en memoria para cada test.
    Se limpia automáticamente después de cada test.
    """
    # Crear engine en memoria (SQLite)
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Crear todas las tablas
    SQLModel.metadata.create_all(engine)

    # Crear sesión
    with Session(engine) as session:
        yield session


# Fixture para cliente de pruebas
@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Crea un cliente de pruebas de FastAPI con la sesión de test.
    """

    # Override de la dependencia get_session
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# Fixture para crear usuarios de prueba
@pytest.fixture(name="usuario_test")
def usuario_test_fixture(session: Session):
    """
    Crea un usuario de prueba en la base de datos.
    """
    usuario = Usuario(nombre="Usuario Test", correo="usuario@test.com")
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


# Fixture para crear canciones de prueba
@pytest.fixture(name="cancion_test")
def cancion_test_fixture(session: Session):
    """
    Crea una cancion de prueba en la base de datos.
    """
    cancion = Cancion(
        titulo="Canción Test",
        artista="Artista Test",
        album="Album Test",
        duracion=240,
        año=2020,
        genero="Rock",
    )
    session.add(cancion)
    session.commit()
    session.refresh(cancion)
    return cancion


# Fixture para crear favorito de prueba
@pytest.fixture(name="favorito_test")
def favorito_test_fixture(
    session: Session, usuario_test: Usuario, cancion_test: Cancion
):
    """
    Crea un favorito de prueba en la base de datos.
    """
    favorito = Favorito(id_usuario=usuario_test.id, id_cancion=cancion_test.id)
    session.add(favorito)
    session.commit()
    session.refresh(favorito)
    return favorito


# =============================================================================
# TESTS DE USUARIOS
# =============================================================================


class TestUsuarios:
    """Tests para los endpoints de usuarios."""

    def test_listar_usuarios(self, client: TestClient):
        """Test para GET /api/usuarios"""
        response = client.get("/api/usuarios")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_crear_usuario(self, client: TestClient):
        """Test para POST /api/usuarios"""
        usuario_data = {"nombre": "Juan Pérez", "correo": "juan@example.com"}
        response = client.post("/api/usuarios/", json=usuario_data)
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == usuario_data["nombre"]
        assert data["correo"] == usuario_data["correo"]
        assert "id" in data
        assert "fecha_registro" in data

    def test_crear_usuario_correo_duplicado(
        self, client: TestClient, usuario_test: Usuario
    ):
        """Test para verificar que no se permiten correos duplicados"""
        usuario_data = {
            "nombre": "Otro Usuario",
            "correo": usuario_test.correo,  # Mismo correo
        }
        response = client.post("/api/usuarios/", json=usuario_data)
        assert response.status_code == 400
        assert "correo electrónico ya está registrado" in response.json()["detail"]

    def test_obtener_usuario(self, client: TestClient, usuario_test: Usuario):
        """Test para GET /api/usuarios/{id}"""
        response = client.get(f"/api/usuarios/{usuario_test.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == usuario_test.id
        assert data["nombre"] == usuario_test.nombre
        assert data["correo"] == usuario_test.correo

    def test_obtener_usuario_no_existe(self, client: TestClient):
        """Test para verificar error 404 con usuario inexistente"""
        response = client.get("/api/usuarios/999")
        assert response.status_code == 404
        assert "Usuario no encontrado" in response.json()["detail"]

    def test_actualizar_usuario(self, client: TestClient, usuario_test: Usuario):
        """Test para PUT /api/usuarios/{id}"""
        datos_actualizacion = {"nombre": "Usuario Actualizado"}
        response = client.put(
            f"/api/usuarios/{usuario_test.id}", json=datos_actualizacion
        )
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == datos_actualizacion["nombre"]
        assert data["correo"] == usuario_test.correo  # No cambió

    def test_eliminar_usuario(self, client: TestClient, usuario_test: Usuario):
        """Test para DELETE /api/usuarios/{id}"""
        response = client.delete(f"/api/usuarios/{usuario_test.id}")
        assert response.status_code == 204

        # Verificar que el usuario fue eliminado
        response = client.get(f"/api/usuarios/{usuario_test.id}")
        assert response.status_code == 404


# =============================================================================
# TESTS DE canciónS
# =============================================================================


class TestCanciones:
    """Tests para los endpoints de canciones."""

    def test_listar_canciones(self, client: TestClient):
        """Test para GET /api/canciones"""
        response = client.get("/api/canciones")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_crear_cancion(self, client: TestClient):
        """Test para POST /api/canciones"""
        cancion_data = {
            "titulo": "Bohemian Rhapsody",
            "artista": "Queen",
            "album": "A Night at the Opera",
            "duracion": 355,
            "año": 1975,
            "genero": "Rock",
        }
        response = client.post("/api/canciones/", json=cancion_data)
        assert response.status_code == 201
        data = response.json()
        assert data["titulo"] == cancion_data["titulo"]
        assert data["artista"] == cancion_data["artista"]
        assert "id" in data
        assert "fecha_creacion" in data

    def test_obtener_cancion(self, client: TestClient, cancion_test: Cancion):
        """Test para GET /api/canciones/{id}"""
        response = client.get(f"/api/canciones/{cancion_test.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == cancion_test.id
        assert data["titulo"] == cancion_test.titulo
        assert data["artista"] == cancion_test.artista

    def test_actualizar_cancion(self, client: TestClient, cancion_test: Cancion):
        """Test para PUT /api/canciones/{id}"""
        datos_actualizacion = {"titulo": "Canción Actualizada", "genero": "Pop"}
        response = client.put(
            f"/api/canciones/{cancion_test.id}", json=datos_actualizacion
        )
        assert response.status_code == 200
        data = response.json()
        assert data["titulo"] == datos_actualizacion["titulo"]
        assert data["genero"] == datos_actualizacion["genero"]
        assert data["artista"] == cancion_test.artista  # No cambió

    def test_eliminar_cancion(self, client: TestClient, cancion_test: Cancion):
        """Test para DELETE /api/canciones/{id}"""
        response = client.delete(f"/api/canciones/{cancion_test.id}")
        assert response.status_code == 204

        # Verificar que la canción fue eliminada
        response = client.get(f"/api/canciones/{cancion_test.id}")
        assert response.status_code == 404

    def test_buscar_canciones(self, client: TestClient, cancion_test: Cancion):
        """Test para GET /api/canciones/buscar"""
        # Buscar por título
        response = client.get(f"/api/canciones/buscar?titulo={cancion_test.titulo}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["titulo"] == cancion_test.titulo

    def test_buscar_canciones_multiples_filtros(self, client: TestClient):
        """Test para búsqueda con múltiples parámetros"""
        # Crear una canción específica para buscar
        cancion_data = {
            "titulo": "Stairway to Heaven",
            "artista": "Led Zeppelin",
            "album": "Led Zeppelin IV",
            "duracion": 482,
            "año": 1971,
            "genero": "Rock",
        }
        client.post("/api/canciones/", json=cancion_data)

        # Buscar con múltiples filtros
        response = client.get(
            "/api/canciones/buscar?artista=Led Zeppelin&genero=Rock&año=1971"
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1


# =============================================================================
# TESTS DE FAVORITOS
# =============================================================================


class TestFavoritos:
    """Tests para los endpoints de favoritos."""

    def test_listar_favoritos(self, client: TestClient):
        """Test para GET /api/favoritos"""
        response = client.get("/api/favoritos")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_crear_favorito(
        self, client: TestClient, usuario_test: Usuario, cancion_test: Cancion
    ):
        """Test para POST /api/favoritos"""
        favorito_data = {"id_usuario": usuario_test.id, "id_cancion": cancion_test.id}
        response = client.post("/api/favoritos/", json=favorito_data)
        assert response.status_code == 201
        data = response.json()
        assert data["id_usuario"] == favorito_data["id_usuario"]
        assert data["id_cancion"] == favorito_data["id_cancion"]
        assert "id" in data
        assert "fecha_marcado" in data

    def test_crear_favorito_duplicado(
        self, client: TestClient, usuario_test: Usuario, cancion_test: Cancion
    ):
        """Test para verificar que no se permiten favoritos duplicados"""
        favorito_data = {"id_usuario": usuario_test.id, "id_cancion": cancion_test.id}
        # Crear el primer favorito
        response1 = client.post("/api/favoritos/", json=favorito_data)
        assert response1.status_code == 201

        # Intentar crear el mismo favorito de nuevo
        response2 = client.post("/api/favoritos/", json=favorito_data)
        assert response2.status_code == 400
        assert "ya está marcada como favorita" in response2.json()["detail"]

    def test_eliminar_favorito(
        self,
        client: TestClient,
        favorito_test: Favorito,
    ):
        """Test para DELETE /api/favoritos/{id}"""
        response = client.delete(f"/api/favoritos/{favorito_test.id}")
        assert response.status_code == 204

        # Verificar que el favorito fue eliminado
        response = client.get(f"/api/favoritos/{favorito_test.id}")
        assert response.status_code == 404

    def test_marcar_favorito_usuario(
        self, client: TestClient, usuario_test: Usuario, cancion_test: Cancion
    ):
        """Test para POST /api/favoritos/{id_usuario}/canciones/{id_cancion}"""
        response = client.post(
            f"/api/favoritos/{usuario_test.id}/canciones/{cancion_test.id}"
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id_usuario"] == usuario_test.id
        assert data["id_cancion"] == cancion_test.id

    def test_listar_favoritos_usuario(
        self,
        client: TestClient,
        usuario_test: Usuario,
        favorito_test: Favorito,
    ):
        """Test para GET /api/usuarios/{id}/favoritos"""
        response = client.get(f"/api/usuarios/{usuario_test.id}/favoritos")
        assert response.status_code == 200
        data = response.json()
        assert "favoritos" in data
        assert len(data["favoritos"]) >= 1


# =============================================================================
# TESTS DE INTEGRACIÓN
# =============================================================================


class TestIntegracion:
    """Tests de integración que prueban flujos completos."""

    def test_flujo_completo(self, client: TestClient):
        """Test que verifica el flujo completo de la aplicación"""
        # 1. Crear usuario
        usuario_data = {
            "nombre": "Usuario Integración",
            "correo": "integracion@test.com",
        }
        response_usuario = client.post("/api/usuarios/", json=usuario_data)
        assert response_usuario.status_code == 201
        usuario = response_usuario.json()

        # 2. Crear canción
        cancion_data = {
            "titulo": "Canción Integración",
            "artista": "Artista Integración",
            "album": "Album Integración",
            "duracion": 180,
            "año": 2023,
            "genero": "Pop",
        }
        response_cancion = client.post("/api/canciones/", json=cancion_data)
        assert response_cancion.status_code == 201
        cancion = response_cancion.json()

        # 3. Marcar como favorito
        favorito_data = {"id_usuario": usuario["id"], "id_cancion": cancion["id"]}
        response_favorito = client.post("/api/favoritos/", json=favorito_data)
        assert response_favorito.status_code == 201

        # 4. Verificar que aparece en favoritos del usuario
        response_favoritos = client.get(f"/api/usuarios/{usuario['id']}/favoritos")
        assert response_favoritos.status_code == 200
        data = response_favoritos.json()
        assert len(data["favoritos"]) == 1


# =============================================================================
# TESTS DE VALIDACIÓN
# =============================================================================


class TestValidacion:
    """Tests para validaciones de datos."""

    def test_email_invalido(self, client: TestClient):
        """Test para verificar validación de email"""
        usuario_data = {
            "nombre": "Usuario Test",
            "correo": "email-invalido",  # Email sin formato válido
        }
        response = client.post("/api/usuarios/", json=usuario_data)
        assert response.status_code == 422  # Validation error

    def test_año_cancion_invalido(self, client: TestClient):
        """Test para verificar validación de año"""
        cancion_data = {
            "titulo": "Canción Futura",
            "artista": "Artista Futura",
            "album": "Album Futuro",
            "duracion": 240,
            "año": 2030,  # Año futuro
            "genero": "Futurista",
        }
        response = client.post("/api/canciones/", json=cancion_data)
        assert response.status_code == 422  # Validation error

    def test_campos_requeridos(self, client: TestClient):
        """Test para verificar que los campos requeridos son obligatorios"""
        # Test sin nombre de usuario
        usuario_data_incompleto = {
            "correo": "test@example.com"
            # Falta "nombre"
        }
        response = client.post("/api/usuarios/", json=usuario_data_incompleto)
        assert response.status_code == 422

        # Test sin título de canción
        cancion_data_incompleto = {
            "artista": "Artista Test",
            "album": "Album Test",
            "duracion": 240,
            "año": 2020,
            "genero": "Rock",
            # Falta "titulo"
        }
        response = client.post("/api/canciones/", json=cancion_data_incompleto)
        assert response.status_code == 422
