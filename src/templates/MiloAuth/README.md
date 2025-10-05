# MiloAuth - Templates de Autenticación

Esta carpeta contiene todos los templates HTML relacionados con el sistema de autenticación de MiloApps.

## Estructura de Archivos

### Templates de Login y Registro

- `login.html` - Página principal de inicio de sesión
- `login_backup.html` - Respaldo del template de login
- `register.html` - Página de registro de nuevos usuarios

### Gestión de Contraseñas

- `forgot_password.html` - Formulario de recuperación de contraseña
- `forgot_password_adapted.html` - Versión adaptada del formulario
- `change_password.html` - Cambio de contraseña para usuarios logueados

### Gestión de Perfil

- `profile.html` - Página de perfil del usuario

### Autenticación de Dos Factores (2FA)

- `two_factor.html` - Página principal de 2FA
- `two_factor_setup.html` - Configuración inicial de 2FA
- `two_factor_disable.html` - Desactivación de 2FA

### Template Base

- `base_auth.html` - Template base para todas las páginas de autenticación

## Uso en el Código

Todos los templates de esta carpeta se referencian desde `auth_routes.py` usando la ruta `MiloAuth/nombre_template.html`:

```python
return render_template('MiloAuth/login.html', form=form, config=load_app_config())
```

## Características del Sistema MiloAuth

- ✅ Auto-logout con aviso de 5 minutos
- ✅ Control de sesión única (UUID-based)
- ✅ Autenticación de dos factores
- ✅ Recuperación de contraseñas por email
- ✅ Templates profesionales con Bootstrap 5
- ✅ Toggle de visibilidad de contraseñas
- ✅ Auditoría completa de eventos
- ✅ Gestión de usuarios administrativa
