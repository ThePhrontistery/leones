# AI Web Template

Un proyecto base minimalista que combina **FastAPI** (backend Python), **Jinja2** (motor de plantillas HTML), y **HTMX** (interactividad web reactiva), todo gestionado con [uv](https://github.com/astral-sh/uv).
Incluye además soporte para **TailwindCSS** (estilos modernos) y carga automática de variables de entorno.

---

## Requisitos previos

* **Python 3.12 o superior**
  Recomendamos usar siempre una versión reciente de Python para asegurar compatibilidad.
* **uv**
  Es una herramienta moderna de gestión de entornos y dependencias para Python.
  Instálala una vez con:

  ```bash
  pipx install uv
  ```

  Más información: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)

---

## Primeros pasos

```bash
# 1. Clona el repositorio y entra en la carpeta del proyecto
git clone <repo-url> ai-web-template
cd ai-web-template

# 2. Instala automáticamente todas las dependencias, crea el entorno virtual y el archivo de lock
uv sync

# 3a. Inicia el servidor de desarrollo (modo básico)
python -m app

# 3b. O bien, inicia el servidor con recarga automática (hot reload)
uv run -- uvicorn app.__main__:app --reload
```

* El comando `uv sync` lee el archivo **pyproject.toml**, instala todas las dependencias necesarias, crea un entorno virtual aislado, y guarda el estado en **uv.lock**.
* Si quieres desarrollo con recarga automática (ideal mientras editas el código), usa la opción 3b.

---

## Cómo añadir o actualizar dependencias

Cuando necesites nuevas librerías o quieras actualizar alguna existente, utiliza:

```bash
uv add nombre_paquete@latest    # Añade y bloquea la versión más reciente
uv sync                        # Sincroniza el entorno con el lockfile
```

Esto asegura que todo el equipo utilice exactamente las mismas versiones.

---

## Variables de entorno

Las variables de entorno (por ejemplo, puertos, modo desarrollo/producción, etc.) se gestionan en un archivo `.env`.

1. Copia el ejemplo y edítalo según tus necesidades:

   ```bash
   cp .env.example .env
   ```
2. Estas variables se cargarán automáticamente al arrancar la app, gracias a `python-dotenv` (ver `app/__init__.py`).

---

## Arquitectura y buenas prácticas

* El backend utiliza **FastAPI**, con rutas definidas en la carpeta `app/api/`.
* Las vistas HTML se gestionan con **Jinja2** en la carpeta `templates/`, extendiendo siempre `base.html`.
* La interactividad se basa en **HTMX** para peticiones asíncronas sin recargar la página.
* Los estilos están hechos con **TailwindCSS** (CDN).
* El proyecto está pensado para un desarrollo limpio, modular y fácil de mantener.

---

## Instrucciones personalizadas para GitHub Copilot

En el archivo `.github/copilot-instructions.md` encontrarás detalles sobre la arquitectura y recomendaciones de uso, para que GitHub Copilot genere código siguiendo las convenciones y tecnologías del proyecto.

---

## Propósito de Negocio de Metasketch

Metasketch es una herramienta colaborativa diseñada para transformar ideas, requisitos y documentación en diseños funcionales vivos. Su objetivo es facilitar la creación, edición y exportación de documentos funcionales mediante un enfoque conversacional (Vibecoding), permitiendo que analistas y especialistas funcionales colaboren con IA para construir aplicaciones y corregir errores sin necesidad de conocimientos avanzados de programación. El proceso es iterativo, ágil y centrado en la colaboración y la inmediatez entre idea, revisión y entrega.

## Principales funcionalidades de Metasketch

- **Login de usuarios:** Acceso seguro a la aplicación mediante usuario y contraseña.
- **Panel de carga de documentos:** Permite crear proyectos, cargar y organizar documentos, y gestionar su ciclo de vida.
- **Árbol de contenidos:** Visualización y edición estructurada de los documentos mediante un árbol interactivo.
- **Editor Markdown con vista previa:** Edición de los contenidos funcionales con ayuda de la IA y visualización en tiempo real.
- **Chat lateral con IA:** Interacción conversacional para sugerencias, reorganización y mejora de los textos funcionales.
- **Botón de exportación:** Generación automática de documentos profesionales en Word o PDF a partir del diseño funcional vivo.
- **Gestión de bloqueos y permisos:** Control de acceso y edición concurrente de proyectos y documentos.

---

## Resumen de arquitectura y stack actual

- **Frontend:** Plantillas Jinja2 en `templates/`, recursos estáticos en `static/`, interactividad con HTMX, estilos con Tailwind CSS (CDN).
- **Backend:** FastAPI (Python 3.12+), rutas en `app/api/`, lógica en `app/services/`, modelos en `app/models/`, base de datos en `app/db/`.
- **Gestión de dependencias:** `pyproject.toml` y `uv sync`.
- **Variables de entorno:** `.env` y `python-dotenv`.

Para más detalles sobre la arquitectura actual, consulta el documento [Architecture_Today.md](./Architecture_Today.md).

Para más detalles sobre las buenas prácticas y principios aplicados, consulta el documento [BestPractices_Today.md](./BestPractices_Today.md).

---

## Documentación adicional

- [Documentación del Modelo de Datos](./Documentation_DataModel.md)
- [Documentación de Funcionalidades Principales](./Documentacion_Funcionalidades_principales.md)
- [Propuestas de Mejora para la Documentación](./Documentation_improvements_ToBe.md)

### Planes de pruebas por funcionalidad
- [Login de usuarios](./app/tests/testplan_login.md)
- [Panel de carga de documentos](./app/tests/testplan_upload.md)
- [Árbol de contenidos](./app/tests/testplan_arbol_contenidos.md)
- [Editor Markdown con vista previa](./app/tests/testplan_editor_markdown.md)
- [Chat lateral con IA](./app/tests/testplan_chat_ia.md)
- [Exportación (Word/PDF)](./app/tests/testplan_export.md)
