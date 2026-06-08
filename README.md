# Portal de Validaciones — Backend

Backend del **Portal Web de Validaciones**, desarrollado con **Django REST Framework**. Permite que locatarios, comercios y usuarios autorizados consulten boletos y apliquen validaciones/descuentos sobre múltiples sistemas de estacionamiento (Designa, DataPark, ZEAG, Meypar, entre otros).

---

## Objetivo

Construir un backend centralizado y extensible para:

- Gestionar **usuarios, roles y permisos** por tenant.
- Administrar **locatarios/comercios** autorizados y sus estacionamientos.
- **Consultar boletos** en tiempo real desde cualquier sistema externo conectado.
- **Aplicar validaciones o descuentos** de forma segura y trazable.
- Registrar **auditoría completa** de cada operación.
- Generar **reportes administrativos**.
- Integrarse con **múltiples proveedores externos** sin modificar la lógica de negocio.

---

## Principio arquitectónico

```
El portal maneja el negocio.
Las integraciones manejan la comunicación técnica con cada proveedor externo.
```

Cada sistema externo (Designa, DataPark, etc.) tiene su propio adaptador que implementa una interfaz común (`IParkingProvider`). El dispatcher elige el proveedor correcto en tiempo de ejecución según la configuración del estacionamiento.

```
Solicitud del usuario
       ↓
Validation Service  (lógica de negocio)
       ↓
Integration Dispatcher  (orquestador)
       ↓
Provider Registry  (fábrica de proveedores)
       ↓
Provider concreto (ej. DesignaProvider)
       ↓
API del sistema externo de estacionamiento
```

---

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Framework | Django 5.2+ |
| API | Django REST Framework 3.15+ |
| Base de datos | PostgreSQL (psycopg v3) |
| HTTP (sync/async) | requests + httpx |
| Encriptación de campos | cryptography |
| Config de entorno | django-environ |
| Servidor de producción | Gunicorn + WhiteNoise |

---

## Estructura del proyecto

```
backend/
├── config/
│   ├── settings/
│   │   ├── base.py          # Configuración base compartida
│   │   ├── local.py         # Desarrollo local (DEBUG=True)
│   │   └── production.py    # Producción (headers de seguridad)
│   ├── urls.py
│   └── wsgi.py / asgi.py
├── apps/
│   ├── accounts/            # Usuarios, roles y permisos (pendiente)
│   ├── audit/               # Auditoría de operaciones (pendiente)
│   ├── integrations/        # Capa de integración con sistemas externos
│   │   ├── base.py          # Interfaz IParkingProvider
│   │   ├── registry.py      # Registro de proveedores (patrón Factory)
│   │   ├── dispatcher.py    # Dispatcher de integraciones
│   │   ├── dtos.py          # Data Transfer Objects internos
│   │   ├── exceptions.py    # Jerarquía de excepciones de integración
│   │   └── clients/
│   │       ├── designa/     # Adaptador Designa (mock activo)
│   │       ├── datapark/    # Pendiente
│   │       └── zeag/        # Pendiente
│   ├── parking_sites/       # Unidades de estacionamiento
│   ├── reports/             # Reportes y exportaciones (pendiente)
│   ├── tenants/             # Locatarios / comercios
│   └── validations/         # Lógica central de validaciones
│       ├── models.py        # ValidationType, ValidationLog
│       ├── services.py      # TicketLookupService, ApplyValidationService
│       ├── views.py         # TicketLookupAPIView, ApplyValidationAPIView
│       └── serializers.py
└── requirements/
    ├── base.txt
    ├── local.txt
    └── production.txt
```

---

## Endpoints disponibles

| Método | URL | Descripción |
|---|---|---|
| `POST` | `/api/validations/tickets/lookup/` | Consulta un boleto y retorna opciones de validación disponibles |
| `POST` | `/api/validations/apply/` | Aplica una validación/descuento a un boleto |

### Ejemplo — Consulta de boleto

```json
POST /api/validations/tickets/lookup/
{
  "parking_site_id": 1,
  "ticket_number": "T-00123"
}
```

### Ejemplo — Aplicar validación

```json
POST /api/validations/apply/
{
  "parking_site_id": 1,
  "ticket_number": "T-00123",
  "validation_type_id": 3
}
```

---

## Instalación y desarrollo local

### Requisitos previos

- Python 3.11+
- PostgreSQL 14+

### Configuración

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd backend

# 2. Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # macOS/Linux

# 3. Instalar dependencias
pip install -r requirements/local.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores locales

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Iniciar servidor
python manage.py runserver
```

### Variables de entorno principales (`.env`)

```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=web_validations
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
FIELD_ENCRYPTION_KEY=change-me
```

---

## Modelos principales

### `ValidationType`
Tipos de validación disponibles (descuentos, cortesías, etc.). Se asocian a tenants y estacionamientos.

### `ValidationLog`
Registro inmutable de cada operación de validación. Incluye montos originales/finales, referencia del sistema externo, payload de request/response y estado del resultado.

### `IntegrationConfig`
Configuración de conexión a un sistema externo. Almacena credenciales encriptadas, URL base, tipo de autenticación y parámetros extra en JSON.

### `ParkingSite`
Unidad de estacionamiento. Se asocia a una `IntegrationConfig` y a uno o más tenants.

### `Tenant`
Locatario o comercio autorizado. Define qué tipos de validación puede aplicar y en qué estacionamientos opera.

---

## Agregar un nuevo proveedor de integración

1. Crear el directorio `apps/integrations/clients/<nombre_proveedor>/`.
2. Implementar la clase adaptadora heredando de `IParkingProvider` (`base.py`).
3. Registrar el proveedor en `apps/integrations/registry.py`.
4. Agregar el `system_type` correspondiente en el modelo `IntegrationConfig`.

No se requiere modificar la lógica de negocio ni los endpoints existentes.

---

## Estado actual del proyecto

| Módulo | Estado |
|---|---|
| Estructura base | Completo |
| Modelos principales | Completo |
| Endpoints de validación | Completo (con mock) |
| Capa de integraciones | Arquitectura completa, Designa en mock |
| Autenticación / Autorización | Pendiente |
| Panel de administración | Básico (Django Admin) |
| Reportes | Pendiente |
| Tests | Pendiente |
| Documentación de API | Pendiente |
| Dockerización | Pendiente |
