# Plan de Pruebas — Editor Markdown con Vista Previa

## Objetivo
Asegurar la edición, guardado y previsualización de documentos Markdown.

## Casos de Prueba

1. **Edición y guardado exitoso**
   - Dado: Documento funcional abierto
   - Cuando: Se edita y guarda
   - Entonces: Cambios persistidos

2. **Vista previa**
   - Dado: Documento con Markdown
   - Cuando: Se pulsa "Preview"
   - Entonces: Renderizado fiel

3. **Errores de guardado**
   - Dado: Fallo de conexión o validación
   - Cuando: Se intenta guardar
   - Entonces: Mensaje de error

## NFR y Seguridad
- Escapado de contenido
- Control de acceso a edición
- Rendimiento en documentos grandes

## Evidencias
- Capturas de pantalla
- Comparación entre Markdown y preview
