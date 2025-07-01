# Documentación del Modelo de Datos — leones.db

## Tablas y Campos

### 1. `users`
- **id**: Integer, clave primaria, autoincremental, indexada.
- **user**: String, único, no nulo. Nombre de usuario.
- **password**: String, no nulo. Contraseña cifrada.

### 2. `uploaded_files`
- **id**: Integer, clave primaria, autoincremental, indexada.
- **filename**: String, no nulo. Nombre del archivo subido.
- **file_path**: String, no nulo. Ruta física del archivo en el sistema.
- **categoria**: String, no nulo. Categoría del documento.
- **descripcion**: String, opcional. Descripción del archivo.
- **proyecto**: String, no nulo, por defecto “demo_metasketch”. Nombre del proyecto asociado.
- **upload_time**: DateTime, fecha y hora de subida (por defecto, actual).

### 3. `markdown_documents`
- **id**: Integer, clave primaria, autoincremental, indexada.
- **content**: Text, no nulo. Contenido markdown del documento.

---

## Relaciones

Actualmente, las tablas no tienen claves foráneas explícitas, pero conceptualmente:
- `uploaded_files.proyecto` puede asociarse a un proyecto (string).
- `uploaded_files` y `markdown_documents` pueden estar relacionados a nivel de aplicación, pero no a nivel de base de datos.

---

## Diagrama de Entidad-Relación (Mermaid)

Sugerencia: Copia este código mermaid y pégalo en [Mermaid Live Editor](https://mermaid.live/). Te creará el modelo E/R de forma visual.

```mermaid
erDiagram
    users {
        INTEGER id PK
        STRING user UNIQUE
        STRING password
    }
    uploaded_files {
        INTEGER id PK
        STRING filename
        STRING file_path
        STRING categoria
        STRING descripcion
        STRING proyecto
        DATETIME upload_time
    }
    markdown_documents {
        INTEGER id PK
        TEXT content
    }
```

---

¿Quieres que te ayude a mejorar el modelo, añadir relaciones o documentar posibles migraciones futuras?
