# Plan de Pruebas — Login de Usuarios

## Objetivo
Verificar el correcto funcionamiento del sistema de autenticación y control de acceso.

## Casos de Prueba

1. **Login exitoso**
   - Dado: Usuario y contraseña válidos
   - Cuando: Se envía el formulario de login
   - Entonces: Acceso concedido, redirección a la home

2. **Login fallido (usuario incorrecto)**
   - Dado: Usuario inexistente
   - Cuando: Se envía el formulario
   - Entonces: Mensaje de error adecuado

3. **Login fallido (contraseña incorrecta)**
   - Dado: Usuario válido, contraseña incorrecta
   - Cuando: Se envía el formulario
   - Entonces: Mensaje de error adecuado

4. **Logout**
   - Dado: Usuario autenticado
   - Cuando: Pulsa "Salir"
   - Entonces: Sesión cerrada, redirección a login

5. **Protección de rutas**
   - Dado: Usuario no autenticado
   - Cuando: Accede a rutas protegidas
   - Entonces: Redirección a login

## NFR y Seguridad
- Verificar hash de contraseñas
- Probar bloqueo tras intentos fallidos
- Validar protección CSRF

## Evidencias
- Capturas de pantalla de cada caso
- Logs de sesión
