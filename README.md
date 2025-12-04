# MARVEL API

Proyecto desarrollado con **FastAPI**, **SQLAlchemy** y **SQLite** (y otras librerías) para gestionar personajes, equipos e identidades secretas del universo Marvel.

## Ejecución

1. **Clonar repositorio**:

bash
git clone <URL_DEL_REPOSITORIO>
cd MarvelAPI_1_0

**Entorno virtual (opcional)**:
bash
python -m venv venv
.\venv\Scripts\activate  

**Instalar dependencias**:

bash
pip install -r requirements.txt

**Ejecutar servidor**:

bash
uvicorn main:app --reload
Abrir documentación de la API:
http://127.0.0.1:8000/docs

**¿Qué hace el proyecto?**
Esta API permite gestionar diferentes aspectos del universo Marvel:

**Personajes**: Crear, listar y buscar personajes con su alias, alineamiento, descripción e imagen.

**Equipos**: Gestionar equipos con su fundador, fecha de fundación, descripción, miembros e imagen.

**Identidades secretas**: Asociar nombres reales, fecha y lugar de nacimiento a los personajes.

**Relaciones Personaje–Equipo**: Asociar personajes a equipos.

**Validaciones**
Se utilizan modelos Pydantic (schemas.py) y Pydantic-settings para validar la información que se ingresa y asegurar que los datos sean correctos antes de almacenarlos en la base de datos.

**Códigos de respuesta de la API**
400 (Bad Request) → Se envió un dato incorrecto o incompleto. Por ejemplo, un campo obligatorio vacío o un dato negativo donde no corresponde.

404 (Not Found) → El recurso solicitado no existe. Ejemplo: consultar un personaje con un ID inexistente.

409 (Conflict) → Conflicto con datos existentes. Ejemplo: crear un equipo con un nombre que ya existe.

Otros códigos que indican éxito:

200 (Ok) → Operación ejecutada correctamente.

201 (Created) → Registro creado exitosamente.

## Funcionalidad del proyecto
**Personajes**:
Método	Endpoint	        Descripción
POST	/characters/new	    Crear un nuevo personaje
GET     /characters	        Listar personajes (con búsqueda por nombre)

**Equipos**:
Método	Endpoint	    Descripción
POST	/teams/new	    Crear un nuevo equipo
GET     /teams	        Listar equipos
GET	    /teams/{id}	    Obtener información de un equipo
PUT	    /teams/{id}	    Actualizar un equipo
DELETE	/teams/{id}	    Eliminar un equipo

**Identidades secretas**:
Método	Endpoint	            Descripción
POST	/identities/new	        Crear identidad secreta
GET	    /identities	Listar      identidades
GET	    /identities/{id}	    Obtener identidad de un personaje

**Relaciones Personaje–Equipo**:
Método	Endpoint	            Descripción
POST	/character_team/new	    Crear relación personaje–equipo
GET	    /character_team/list	Listar todas las relaciones

## Tecnologías usadas
Python 3.13

FastAPI → Framework web

Uvicorn → Servidor ASGI

SQLAlchemy → ORM para base de datos

Pydantic → Validación de datos

Pydantic-settings → Configuración y variables de entorno

ReportLab → Generación de PDFs

python-dotenv → Cargar variables de entorno desde .env

Supabase → Backend as a Service 

Jinja2 → Plantillas HTML

aiofiles → Manejo de archivos asíncronos

Pandas → Manejo de datos en tablas

OpenPyXL → Leer y escribir archivos Excel

XlsxWriter → Generar Excel con formato

psycopg2-binary → Conexión con PostgreSQL

python-multipart → Subida de archivos en formularios

Clever Cloud → Plataforma de despliegue en la nube

Render → Plataforma de despliegue en la nube