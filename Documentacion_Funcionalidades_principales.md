# Documentación de Funcionalidades Principales — Metasketch

Este documento detalla cada funcionalidad principal de la aplicación Metasketch, su implementación, componentes, endpoints, archivos implicados, criterios de completitud, sugerencias de documentación, testing y requisitos NFR.

---

## 1. Login de usuarios

**Descripción:** Permite el acceso seguro a la aplicación mediante usuario y contraseña. Gestiona sesiones y control de acceso.

- **Componentes Front:**
  - `templates/login.html` (formulario de login)
  - `templates/base.html` (estructura base, mensajes de error)
- **Endpoints:**
  - `POST /api/auth/login` (`app/api/auth.py`)
  - `GET /login` (renderiza formulario)
  - `POST /logout` (`app/api/logout.py`)
- **Archivos modificados:**
  - `app/api/auth.py`, `app/api/logout.py`, `app/auth/`, `templates/login.html`, `templates/base.html`
- **Criterios de completitud:**
  - El usuario puede iniciar y cerrar sesión correctamente.
  - Mensajes de error claros ante credenciales incorrectas.
  - Sesión protegida y tokens gestionados correctamente.
- **Sugerencias de documentación:**
  - Actualizar README y BestPractices con el flujo de login y seguridad.
- **Testing:**
  - Pruebas unitarias de login/logout en `app/tests/`.
- **NFR:**
  - Seguridad: Hash de contraseñas, protección CSRF, bloqueo tras intentos fallidos.
  - Rendimiento: Respuesta rápida (<500ms).

---

## 2. Panel de carga de documentos

**Descripción:** Permite crear proyectos, cargar documentos, organizarlos y gestionarlos por proyecto y categoría.

- **Componentes Front:**
  - `templates/upload.html` (formulario de carga)
  - `templates/document_list.html` (listado de documentos)
  - `templates/base.html`, `static/document.js`
- **Endpoints:**
  - `GET /upload` (renderiza formulario)
  - `POST /api/document/upload` (`app/api/document.py`)
  - `GET /api/document/list` (listado de documentos)
  - `POST /api/document/delete` (borrado)
- **Archivos modificados:**
  - `app/api/document.py`, `app/services/document_service.py`, `app/db/models.py`, `templates/upload.html`, `templates/document_list.html`, `static/document.js`
- **Criterios de completitud:**
  - El usuario puede crear proyectos y cargar/borrar documentos.
  - Los documentos se asocian correctamente a proyectos y categorías.
  - El árbol de documentos se actualiza dinámicamente.
- **Sugerencias de documentación:**
  - Añadir ejemplos de uso y estructura de proyectos en la documentación.
- **Testing:**
  - Pruebas de subida/borrado en `app/tests/`.
- **NFR:**
  - Seguridad: Validación de tipo y tamaño de archivo, control de acceso.
  - Rendimiento: Subida y listado eficiente de archivos.

---

## 3. Árbol de contenidos (índices/enlaces)

**Descripción:** Visualiza y permite editar la estructura de los documentos funcionales mediante un árbol interactivo.

- **Componentes Front:**
  - `templates/arbol_contenidos.html` (árbol de contenidos)
  - `templates/partials/` (fragmentos de árbol)
  - `static/document.js`
- **Endpoints:**
  - `GET /api/document/tree` (`app/api/document.py`)
  - `POST /api/document/tree/update` (actualización de estructura)
- **Archivos modificados:**
  - `app/api/document.py`, `app/services/document_service.py`, `templates/arbol_contenidos.html`, `static/document.js`
- **Criterios de completitud:**
  - El árbol refleja la estructura real de los documentos.
  - Permite expandir, contraer y reorganizar ítems.
- **Sugerencias de documentación:**
  - Incluir capturas de pantalla y ejemplos de estructura.
- **Testing:**
  - Pruebas de actualización y visualización del árbol.
- **NFR:**
  - Seguridad: Control de permisos sobre edición.
  - Rendimiento: Renderizado eficiente del árbol.

---

## 4. Editor Markdown con vista previa

**Descripción:** Permite editar el contenido funcional con sintaxis Markdown y ver una vista previa en tiempo real.

- **Componentes Front:**
  - `templates/funcional_result.html`, `templates/funcional_result_y_indice.html`
  - `static/guardar_markdown.js`, `static/markdown.js`
- **Endpoints:**
  - `GET /api/markdown/{id}` (`app/api/markdown.py`)
  - `POST /api/markdown/save` (guardar cambios)
  - `POST /api/markdown/preview` (vista previa)
- **Archivos modificados:**
  - `app/api/markdown.py`, `app/services/markdown_funcional_service.py`, `app/db/markdown.py`, `templates/funcional_result.html`, `static/guardar_markdown.js`
- **Criterios de completitud:**
  - El usuario puede editar y guardar contenido Markdown.
  - Vista previa fiel al resultado final.
- **Sugerencias de documentación:**
  - Añadir guía de sintaxis Markdown y ejemplos.
- **Testing:**
  - Pruebas de guardado y preview en `app/tests/`.
- **NFR:**
  - Seguridad: Escapado de contenido, control de acceso.
  - Rendimiento: Renderizado y guardado rápido.

---

## 5. Chat lateral con IA

**Descripción:** Permite interactuar con la IA para obtener sugerencias, reorganizar o mejorar textos funcionales.

- **Componentes Front:**
  - `templates/partials/chat_ia_panel.html`, `templates/chat_result.html`, `static/chat_ia_service.js`
- **Endpoints:**
  - `POST /api/chat/ia` (`app/api/chat_ia_panel.py`)
- **Archivos modificados:**
  - `app/api/chat_ia_panel.py`, `app/services/chat_ia_service.py`, `templates/partials/chat_ia_panel.html`, `static/chat_ia_service.js`
- **Criterios de completitud:**
  - El usuario puede enviar prompts y recibir sugerencias útiles.
  - Las sugerencias pueden trasladarse fácilmente al editor.
- **Sugerencias de documentación:**
  - Documentar ejemplos de prompts y casos de uso.
- **Testing:**
  - Pruebas de integración IA-usuario.
- **NFR:**
  - Seguridad: Filtrado de prompts, protección ante abusos.
  - Rendimiento: Respuesta de IA en <2s.

---

## 6. Botón de exportación (Word/PDF)

**Descripción:** Permite exportar el documento funcional generado a formatos Word o PDF de forma automática.

- **Componentes Front:**
  - `templates/funcional_result.html`, `static/exportar_markdown.js`
- **Endpoints:**
  - `POST /api/export` (`app/api/export.py`)
- **Archivos modificados:**
  - `app/api/export.py`, `app/services/export_service.py`, `static/exportar_markdown.js`
- **Criterios de completitud:**
  - El usuario puede exportar el documento y descargarlo correctamente.
  - El formato exportado es fiel al diseño funcional.
- **Sugerencias de documentación:**
  - Añadir sección de exportación y formatos soportados.
- **Testing:**
  - Pruebas de exportación y validación de archivos generados.
- **NFR:**
  - Seguridad: Validación de permisos de exportación.
  - Rendimiento: Exportación en menos de 5 segundos.

---

> Para cada funcionalidad, se recomienda mantener la documentación actualizada en los archivos relevantes (`README`, `BestPractices`, manuales de usuario) y crear tests automáticos en `app/tests/` para asegurar la calidad y robustez del sistema.
