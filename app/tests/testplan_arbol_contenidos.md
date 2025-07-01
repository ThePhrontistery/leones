# Plan de Pruebas — Árbol de Contenidos

## Objetivo
Verificar la visualización, edición y sincronización del árbol de contenidos.

## Casos de Prueba

1. **Visualización inicial**
   - Dado: Proyecto con documentos
   - Cuando: Se accede al árbol
   - Entonces: Se muestra la estructura correcta

2. **Expandir/contraer nodos**
   - Dado: Árbol con nodos hijos
   - Cuando: Se expande/contrae
   - Entonces: Cambia el estado visual

3. **Reorganización de ítems**
   - Dado: Ítems arrastrables
   - Cuando: Se reordena
   - Entonces: Estructura actualizada

4. **Sincronización con backend**
   - Dado: Cambio en el árbol
   - Cuando: Se guarda
   - Entonces: Persistencia correcta

## NFR y Seguridad
- Control de permisos de edición
- Rendimiento en árboles grandes

## Evidencias
- Capturas de pantalla
- Logs de cambios
