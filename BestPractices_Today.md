# Buenas Prácticas y Principios Aplicados en Leones (Estado Actual)

Este documento resume los principios y buenas prácticas que se han seguido hasta la fecha en el desarrollo de la aplicación **Leones**.

---

## Principios y buenas prácticas aplicadas

- **Separación de responsabilidades:**
  - Backend en `app/` (rutas, lógica, modelos, servicios, utilidades).
  - Plantillas HTML en `templates/`.
  - Recursos estáticos en `static/`.

- **Uso de tecnologías modernas:**
  - **FastAPI** para el backend (asincrónico, tipado, modular).
  - **Jinja2** para plantillas HTML reutilizables y extensibles.
  - **HTMX** para interactividad progresiva y peticiones parciales.
  - **Tailwind CSS** (CDN) para estilos consistentes y modernos.

- **Gestión de dependencias y entorno:**
  - Todas las dependencias se gestionan en `pyproject.toml` y se sincronizan con `uv sync`.
  - Variables de entorno centralizadas en `.env` y cargadas automáticamente.

- **Estructura modular y extensible:**
  - Rutas organizadas por funcionalidad en `app/api/`.
  - Lógica de negocio separada en `app/services/`.
  - Modelos Pydantic en `app/models/`.
  - Utilidades en `app/utils/`.
  - Acceso a base de datos en `app/db/`.

- **Buenas prácticas de desarrollo:**
  - Código Python siguiendo Black y Ruff (formato y linting).
  - Tipado explícito en Python 3.12+.
  - Uso de docstrings y comentarios descriptivos.
  - Plantillas que extienden siempre `base.html`.
  - Uso de includes y partials para fragmentos reutilizables.
  - Evita lógica JS inline; scripts en archivos separados en `static/`.

- **Seguridad y calidad:**
  - Escapado de variables en Jinja2 para evitar XSS.
  - Gestión de autenticación en `app/auth/`.
  - Pruebas en `app/tests/` siguiendo pytest.

---

Este documento refleja el estado actual y servirá de base para futuras refactorizaciones y mejoras estructurales.
