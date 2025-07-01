# Plan de Pruebas — Chat Lateral con IA

## Objetivo
Verificar la interacción usuario-IA y la utilidad de las sugerencias generadas.

## Casos de Prueba

1. **Envío de prompt válido**
   - Dado: Usuario autenticado
   - Cuando: Envía un prompt
   - Entonces: Recibe sugerencia útil

2. **Envío de prompt inválido**
   - Dado: Prompt vacío o malicioso
   - Cuando: Se envía
   - Entonces: Mensaje de error o filtrado

3. **Traslado de sugerencia al editor**
   - Dado: Sugerencia recibida
   - Cuando: Se copia al editor
   - Entonces: Se puede guardar

## NFR y Seguridad
- Filtrado de prompts
- Protección ante abusos
- Respuesta en <2s

## Evidencias
- Capturas de pantalla
- Logs de interacción
