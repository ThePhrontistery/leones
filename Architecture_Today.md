# Arquitectura Actual de Metasketch

Este documento describe en detalle la arquitectura actual de la aplicación Metasketch, cubriendo los principales bloques del sistema.

---

## Frontend

- **Plantillas HTML:**
  - Todas las vistas se encuentran en `templates/`, extendiendo siempre `base.html`.
  - Uso de includes y partials para fragmentos reutilizables.
- **Interactividad:**
  - HTMX importado globalmente en `base.html` para peticiones asíncronas y actualizaciones parciales de la UI.
  - Patrón de enhancement progresivo: la app funciona sin JS, pero mejora con HTMX.
- **Estilos:**
  - Tailwind CSS vía CDN, aplicado a todas las plantillas.
  - No se utiliza CSS personalizado ni frameworks externos.
- **Recursos estáticos:**
  - JS, imágenes y otros assets en la carpeta `static/`, servidos bajo `/static`.
  - Scripts JS en archivos separados, nunca inline.

---

## Backend

- **Framework principal:** FastAPI (Python 3.12+), orientado a desarrollo asíncrono, tipado y modular.
- **Estructura de carpetas:**
  - `app/api/`: Rutas y endpoints organizados por funcionalidad, siguiendo el patrón router modular.
  - `app/services/`: Lógica de negocio desacoplada de las rutas, para facilitar la reutilización y el testeo.
  - `app/models/`: Modelos Pydantic para validación y serialización de datos, y modelos ORM para la base de datos.
  - `app/db/`: Gestión de la base de datos, sesiones, migraciones y utilidades de acceso a datos.
  - `app/auth/`: Lógica de autenticación y autorización, preferentemente OAuth2 con JWT.
  - `app/utils/`: Funciones auxiliares y utilidades generales.
  - `app/middleware/`: Middleware personalizado para FastAPI.
  - `app/config.py`: Configuración centralizada, cargando variables de entorno.
  - `app/logging.py`: Configuración de logs estructurados en formato JSON.
  - `app/tests/`: Pruebas unitarias e integración, siguiendo convenciones pytest.
- **Base de datos:** Soporte para SQLAlchemy ORM con operaciones asíncronas.
- **API:** Endpoints RESTful bajo `/api/...`, devolviendo modelos Pydantic o dicts, con `response_model` para claridad de esquema.
- **Autenticación:** OAuth2 con JWT tokens, gestionado en `app/auth/`.

---

## Gestión de dependencias

- **Gestión centralizada:**
  - Todas las dependencias Python se declaran en `pyproject.toml`.
  - Se utiliza `uv` para instalar, sincronizar y bloquear versiones, asegurando entornos reproducibles.
  - El archivo `uv.lock` garantiza la consistencia entre entornos de desarrollo y producción.
- **Instalación y actualización:**
  - Nuevas dependencias se añaden con `uv add` y se sincronizan con `uv sync`.

---

## Variables de entorno

- **Gestión:**
  - Variables sensibles y de configuración (puertos, modo, claves, etc.) se almacenan en `.env`.
  - Se cargan automáticamente al iniciar la app mediante `python-dotenv` (ver `app/__init__.py`).
- **Ejemplo:**
  - `.env.example` sirve como plantilla para nuevos entornos.
- **Uso:**
  - Todas las configuraciones críticas se leen desde variables de entorno a través de `app/config.py`.

---

Este documento refleja la arquitectura actual y servirá de base para futuras refactorizaciones y mejoras estructurales.
