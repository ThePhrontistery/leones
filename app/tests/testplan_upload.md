# Plan de Pruebas — Panel de Carga de Documentos

## Objetivo
Asegurar la correcta gestión de proyectos y documentos (subida, borrado, asociación a proyectos/categorías).

## Casos de Prueba

1. **Creación de proyecto**
   - Dado: Usuario autenticado
   - Cuando: Crea un nuevo proyecto
   - Entonces: Proyecto aparece en el árbol

2. **Subida de documento válida**
   - Dado: Proyecto existente, archivo válido
   - Cuando: Se sube el archivo
   - Entonces: Documento aparece en el listado

3. **Subida de documento inválida**
   - Dado: Archivo de tipo/tamaño no permitido
   - Cuando: Se intenta subir
   - Entonces: Mensaje de error

4. **Borrado de documento**
   - Dado: Documento existente
   - Cuando: Se borra
   - Entonces: Desaparece del listado

5. **Árbol actualizado**
   - Dado: Se sube o borra un documento
   - Cuando: Se refresca el árbol
   - Entonces: Refleja los cambios

## NFR y Seguridad
- Validar tipo/tamaño de archivo
- Control de acceso a proyectos/documentos

## Evidencias
- Capturas de pantalla
- Logs de operaciones
