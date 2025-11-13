# API de Música

Una [API RESTful](https://aws.amazon.com/es/what-is/restful-api/) para gestionar usuarios, canciones y favoritos. Desarrollada con [FastAPI](https://fastapi.tiangolo.com/), [SQLModel](https://sqlmodel.tiangolo.com/) y [Pydantic](https://docs.pydantic.dev/).

## Descripción

Esta API permite administrar:
- **Usuarios**: crear y gestionar perfiles de usuarios.
- **Canciones**: agregar, actualizar y eliminar canciones con sus metadatos.
- **Favoritos**: gestionar las canciones favoritas de cada usuario.

El proyecto incluye una interfaz de documentación interactiva generada automáticamente con [Swagger](https://swagger.io/) disponible en el *endpoint* `/docs`.

## Estructura del Proyecto

```
lpa2-taller3
├──  README.md            # Este archivo, documentación completa del proyecto
├──  .env                 # Variables de entorno (desarrollo, pruebas, producción)
├──  .gitignore           # Archivos y directorios a ignorar por Git
├──  main.py              # Script principal para ejecutar la aplicación
├──  musica.db            # Base de Datos
├──  app/                 # Código principal de la aplicación
│   ├──  routers/         # Endpoints de la API
│   ├──  models.py        # Modelos de datos SQLModel
│   ├──  database.py      # Configuración de base de datos
│   ├──  config.py        # Configuración de la aplicación
│   └──  __init__.py      # Inicialización del módulo
├── 󰌠 requirements.txt     # Dependencias del proyecto
├── 󰙨 tests
│   └──  test_api.py      # Pruebas Unitarias
└──  utils.py             # Funciones de utilidad

```
## Modelo de Datos

1. **Usuario**:
   - id: Identificador único
   - nombre: Nombre del usuario
   - correo: Correo electrónico (único)
   - fecha_registro: Fecha de registro

2. **Canción**:
   - id: Identificador único
   - titulo: Título de la canción
   - artista: Artista o intérprete
   - album: Álbum al que pertenece
   - duracion: Duración en segundos
   - año: Año de lanzamiento
   - genero: Género musical
   - fecha_creacion: Fecha de creación del registro

3. **Favorito**:
   - id: Identificador único
   - id_usuario: ID del usuario (clave foránea)
   - id_cancion: ID de la canción (clave foránea)
   - fecha_marcado: Fecha en que se marcó como favorito

## Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/Juanrs69/lpa2-taller3.git
   cd lpa2-taller3
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Ajusta las variables de entorno, editando el archivo `.env`

## Ejecución

1. Ejecuta la aplicación:

   ```bash
   uvicorn main:app --reload
   ```

2. Accede a la aplicación:
   - API: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Documentación *Swagger UI*: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Documentación *ReDoc*: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Uso de la API

### Usuarios

- **Listar usuarios**: `GET /api/usuarios`
- **Crear usuario**: `POST /api/usuarios`
- **Obtener usuario**: `GET /api/usuarios/{id}`
- **Actualizar usuario**: `PUT /api/usuarios/{id}`
- **Eliminar usuario**: `DELETE /api/usuarios/{id}`

### Canciones

- **Listar canciones**: `GET /api/canciones`
- **Crear canción**: `POST /api/canciones`
- **Obtener canción**: `GET /api/canciones/{id}`
- **Actualizar canción**: `PUT /api/canciones/{id}`
- **Eliminar canción**: `DELETE /api/canciones/{id}`
- **Buscar canciones**: `GET /api/canciones/buscar?titulo=value&artista=value&genero=value`

### Favoritos

- **Listar favoritos**: `GET /api/favoritos`
- **Marcar favorito**: `POST /api/favoritos`
- **Obtener favorito**: `GET /api/favoritos/{id}`
- **Eliminar favorito**: `DELETE /api/favoritos/{id}`
- **Listar favoritos de usuario**: `GET /api/usuarios/{id}/favoritos`
- **Marcar favorito específico**: `POST /api/usuarios/{id_usuario}/favoritos/{id_cancion}`
- **Eliminar favorito específico**: `DELETE /api/usuarios/{id_usuario}/favoritos/{id_cancion}`

## Desarrollo del Taller

1. Ajustar este `README.md` con los datos del Estudiante

Juan alejandro Ramirez sanchez.

2. Utilizando [DBeaver](https://dbeaver.io/), adiciona 5 usuarios y 10 canciones, directo a las tablas.

3. Adicionar `pre-commit` y `workflow` de GitHub Actions para **ruff** *linter* y *formatter*, y para **pytest**.

4. Busca todos los comentarios `# TODO` y `# FIXME`, realiza los ajustes necesarios, y ejecuta un `commit` por cada uno. Usa Pydantic para la validación de datos.

5. Prueba el funcionamiento del API, desde la documentación *Swagger UI* o *ReDoc*.

6. Desarrolla las pruebas automatizadas para verificar el funcionamiento correcto de la API.

7. Implementar dos (2) de las sugerencias que se presentan a continuación.

## Sugerencias de Mejora

1. **Autenticación y autorización**: Implementar JWT o OAuth2 para proteger los endpoints y asociar los usuarios automáticamente con sus favoritos.

2. **Paginación**: Añadir soporte para paginación en las listas de canciones, usuarios y favoritos para mejorar el rendimiento con grandes volúmenes de datos.

3. **Base de datos en producción**: Migrar a una base de datos más robusta como PostgreSQL o MySQL para entornos de producción.

4. **Docker**: Contenerizar la aplicación para facilitar su despliegue en diferentes entornos.

5. **Registro (logging)**: Implementar un sistema de registro más completo para monitorear errores y uso de la API.

6. **Caché**: Añadir caché para mejorar la velocidad de respuesta en consultas frecuentes.

7. **Estadísticas de uso**: Implementar un sistema de seguimiento para analizar qué canciones son más populares y sugerir recomendaciones basadas en preferencias similares.

8. **Subida de archivos**: Permitir la subida de archivos de audio y gestionar su almacenamiento en un servicio como S3 o similar.

---

## 🛠️ Guía de Desarrollo y Contribución

### 🚀 Configuración de Desarrollo

#### Prerrequisitos
- Python 3.11 o superior
- Git

#### Configuración inicial

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/Juanrs69/lpa2-taller3.git
   cd lpa2-taller3
   ```

2. **Crea y activa el entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   # o
   venv\Scripts\activate  # En Windows
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura pre-commit:**
   ```bash
   pre-commit install
   ```

5. **Ejecuta la aplicación:**
   ```bash
   uvicorn main:app --reload
   ```

### 🔧 Herramientas de Calidad de Código

#### Ruff (Linter y Formatter)
```bash
# Verificar código
ruff check .

# Formatear código
ruff format .

# Arreglar problemas automáticamente
ruff check --fix .
```

#### Pruebas
```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar con cobertura
pytest --cov=app --cov-report=html
```

#### Pre-commit
Los hooks de pre-commit se ejecutan automáticamente antes de cada commit:
- Formato de código con Ruff
- Verificación de linting
- Limpieza de espacios en blanco
- Verificación de archivos YAML/JSON

Para ejecutar manualmente:
```bash
pre-commit run --all-files
```

### 📋 Proceso de Contribución

1. **Fork** el repositorio
2. **Crea una rama** para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. **Realiza tus cambios** siguiendo las convenciones de código
4. **Ejecuta las pruebas**: `pytest`
5. **Ejecuta pre-commit**: `pre-commit run --all-files`
6. **Commit** tus cambios: `git commit -m "feat: descripción del cambio"`
7. **Push** a tu fork: `git push origin feature/nueva-funcionalidad`
8. **Crea un Pull Request**

### 🎯 Convenciones de Código

#### Estilo de Código
- Usamos **Ruff** para formateo y linting
- Longitud máxima de línea: **88 caracteres**
- Quotes: **dobles** (`"`)
- Imports organizados automáticamente

#### Commits
Usamos [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` nueva funcionalidad
- `fix:` corrección de bug
- `docs:` cambios en documentación
- `style:` cambios de formato
- `refactor:` refactoring de código
- `test:` añadir o modificar tests
- `chore:` tareas de mantenimiento

#### Tests
- Escribe tests para nuevas funcionalidades
- Mantén cobertura de código > 80%
- Usa fixtures para datos de prueba
- Nombra tests descriptivamente: `test_crear_usuario_email_duplicado`

### 🚨 CI/CD

Nuestro pipeline de CI/CD incluye:

#### GitHub Actions
- **Linting y Format**: Verifica estilo de código con Ruff
- **Tests**: Ejecuta pytest en Python 3.11 y 3.12
- **Seguridad**: Análisis con Safety y Bandit
- **Build**: Verificación de build en main

#### Pre-commit Hooks
- Formato automático con Ruff
- Verificación de linting
- Validación de archivos YAML/JSON
- Limpieza de espacios en blanco

### 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/Juanrs69/lpa2-taller3/issues)
- **Desarrollador**: Juan Alejandro Ramirez Sanchez
- **Email**: juanalejandro004@gmail.com

### 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
