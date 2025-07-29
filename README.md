# 🕊️ Totus Tuus - App de Consagración Total

Backend API para la aplicación de consagración total a María, siguiendo las enseñanzas de San Luis María Grignion de Montfort.

## 📋 Características

- **Autenticación JWT** con tokens de acceso y refresco
- **Gestión de usuarios** con perfiles y progreso
- **Contenido diario** para 33 días de consagración
- **Seguimiento de progreso** (meditación, video, rosario)
- **Chatbot** que responde como San Luis de Montfort
- **API RESTful** con documentación automática
- **Base de datos PostgreSQL** con migraciones Alembic
- **CORS configurado** para integración con React

## 🚀 Instalación

### Prerrequisitos

- Python 3.8+
- PostgreSQL
- pip

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd backend_consagracion
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp env.example .env
```

Editar `.env` con tus configuraciones:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/totus_tuus_db

# JWT Configuration
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=Totus Tuus - App de Consagración Total

# CORS Configuration
BACKEND_CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# Environment
ENVIRONMENT=development
```

### 5. Configurar base de datos

```bash
# Crear base de datos PostgreSQL
createdb totus_tuus_db

# Ejecutar migraciones
alembic upgrade head

# Poblar con datos de ejemplo
python scripts/populate_db.py
```

### 6. Ejecutar el servidor

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en `http://localhost:8000`

## 📚 Documentación de la API

### Endpoints de Autenticación

#### POST `/api/v1/auth/register`

Registrar un nuevo usuario.

**Body:**

```json
{
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "password": "password123"
}
```

#### POST `/api/v1/auth/login`

Iniciar sesión.

**Body:**

```json
{
  "email": "juan@example.com",
  "password": "password123"
}
```

#### POST `/api/v1/auth/refresh`

Renovar token de acceso.

**Headers:**

```
Authorization: Bearer <refresh_token>
```

### Endpoints de Usuario

#### GET `/api/v1/users/profile`

Obtener perfil del usuario actual.

**Headers:**

```
Authorization: Bearer <access_token>
```

#### PUT `/api/v1/users/profile`

Actualizar perfil del usuario.

**Headers:**

```
Authorization: Bearer <access_token>
```

**Body:**

```json
{
  "name": "Juan Pérez Actualizado",
  "current_day": 5
}
```

#### GET `/api/v1/users/progress`

Obtener progreso del usuario para todos los días.

**Headers:**

```
Authorization: Bearer <access_token>
```

#### POST `/api/v1/users/progress`

Actualizar progreso para un día específico.

**Headers:**

```
Authorization: Bearer <access_token>
```

**Body:**

```json
{
  "day": 5,
  "meditation_completed": true,
  "video_completed": false,
  "rosary_completed": true
}
```

### Endpoints de Contenido

#### GET `/api/v1/content/daily/{day}`

Obtener contenido para un día específico.

#### GET `/api/v1/content/all`

Obtener todo el contenido diario.

### Endpoints de Chat

#### POST `/api/v1/chat/message`

Enviar mensaje al chatbot de San Luis de Montfort.

**Headers:**

```
Authorization: Bearer <access_token>
```

**Body:**

```json
{
  "message": "¿Qué es la consagración total a María?"
}
```

#### GET `/api/v1/chat/history`

Obtener historial de chat del usuario.

**Headers:**

```
Authorization: Bearer <access_token>
```

## 🗄️ Estructura de la Base de Datos

### Tabla: users

- `id`: Primary key
- `name`: Nombre del usuario
- `email`: Email único
- `password_hash`: Contraseña hasheada
- `current_day`: Día actual de la consagración
- `start_date`: Fecha de inicio
- `is_active`: Estado activo
- `created_at`: Fecha de creación
- `updated_at`: Fecha de actualización

### Tabla: daily_content

- `id`: Primary key
- `day`: Día de la consagración (1-33)
- `title`: Título del día
- `description`: Descripción del contenido
- `video_url`: URL del video principal
- `rosary_video_url`: URL del video del rosario
- `meditation_pdf_url`: URL del PDF de meditación
- `mysteries`: Misterios del rosario
- `quote`: Cita del día
- `created_at`: Fecha de creación
- `updated_at`: Fecha de actualización

### Tabla: user_progress

- `id`: Primary key
- `user_id`: Foreign key a users
- `day`: Día de la consagración
- `meditation_completed`: Meditación completada
- `video_completed`: Video completado
- `rosary_completed`: Rosario completado
- `completed_at`: Fecha de completado

### Tabla: chat_history

- `id`: Primary key
- `user_id`: Foreign key a users
- `message`: Mensaje del usuario
- `response`: Respuesta del chatbot
- `timestamp`: Fecha y hora

## 🔧 Comandos Útiles

### Migraciones de Base de Datos

```bash
# Crear nueva migración
alembic revision --autogenerate -m "Descripción del cambio"

# Aplicar migraciones
alembic upgrade head

# Revertir migración
alembic downgrade -1
```

### Poblar Base de Datos

```bash
# Poblar con datos de ejemplo
python scripts/populate_db.py
```

### Ejecutar Tests

```bash
# Instalar dependencias de desarrollo
pip install pytest pytest-asyncio

# Ejecutar tests
pytest
```

## 🛠️ Desarrollo

### Estructura del Proyecto

```
backend_consagracion/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación FastAPI
│   ├── config.py            # Configuración
│   ├── database.py          # Configuración de BD
│   ├── models/              # Modelos SQLAlchemy
│   ├── schemas/             # Esquemas Pydantic
│   ├── api/                 # Rutas de la API
│   ├── services/            # Lógica de negocio
│   └── utils/               # Utilidades
├── alembic/                 # Migraciones
├── scripts/                 # Scripts de utilidad
├── requirements.txt         # Dependencias
├── alembic.ini             # Configuración Alembic
└── README.md               # Documentación
```

### Variables de Entorno

| Variable                      | Descripción                  | Valor por Defecto                                         |
| ----------------------------- | ---------------------------- | --------------------------------------------------------- |
| `DATABASE_URL`                | URL de conexión a PostgreSQL | `postgresql://user:password@localhost:5432/totus_tuus_db` |
| `SECRET_KEY`                  | Clave secreta para JWT       | `your-secret-key-here-make-it-long-and-secure`            |
| `ALGORITHM`                   | Algoritmo JWT                | `HS256`                                                   |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiración token acceso      | `30`                                                      |
| `REFRESH_TOKEN_EXPIRE_DAYS`   | Expiración token refresco    | `7`                                                       |
| `API_V1_STR`                  | Prefijo de la API            | `/api/v1`                                                 |
| `PROJECT_NAME`                | Nombre del proyecto          | `Totus Tuus - App de Consagración Total`                  |
| `ENVIRONMENT`                 | Entorno de ejecución         | `development`                                             |

## 🔒 Seguridad

- **JWT Tokens**: Autenticación segura con tokens de acceso y refresco
- **Password Hashing**: Contraseñas hasheadas con bcrypt
- **CORS**: Configurado para permitir solo orígenes específicos
- **Validación**: Todos los inputs validados con Pydantic
- **Error Handling**: Manejo completo de errores con mensajes en español

## 🧪 Testing

```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest

# Ejecutar tests con coverage
pytest --cov=app
```

## 📦 Despliegue

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Producción

1. Configurar variables de entorno para producción
2. Usar base de datos PostgreSQL en producción
3. Configurar HTTPS
4. Implementar logging y monitoreo
5. Configurar backup de base de datos

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- San Luis María Grignion de Montfort por sus enseñanzas sobre la consagración total a María
- FastAPI por proporcionar un framework moderno y rápido
- La comunidad de desarrolladores que contribuye a las librerías utilizadas

---

**¡Que María, nuestra Madre celestial, bendiga este proyecto y a todos los que lo utilicen!** 🙏
