# Plan de Pruebas — Exportación (Word/PDF)

## Objetivo
Asegurar la correcta exportación y descarga de documentos funcionales en los formatos soportados.

## Casos de Prueba

1. **Exportación exitosa a Word**
   - Dado: Documento funcional generado
   - Cuando: Se pulsa "Exportar Word"
   - Entonces: Descarga correcta, formato fiel

2. **Exportación exitosa a PDF**
   - Dado: Documento funcional generado
   - Cuando: Se pulsa "Exportar PDF"
   - Entonces: Descarga correcta, formato fiel

3. **Error de exportación**
   - Dado: Fallo en el backend o permisos insuficientes
   - Cuando: Se intenta exportar
   - Entonces: Mensaje de error

## NFR y Seguridad
- Validación de permisos
- Exportación en <5s

## Evidencias
- Archivos descargados
- Capturas de pantalla
