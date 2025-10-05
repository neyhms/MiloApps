# MiloAdmin - Templates Administrativos

Esta carpeta contiene todos los templates HTML relacionados con la administración de usuarios y el panel administrativo de MiloApps.

## Estructura de Archivos

### Gestión de Usuarios

- `admin_users.html` - Lista y búsqueda de usuarios del sistema
- `admin_user_detail.html` - Detalles y edición de usuarios individuales

## Uso en el Código

Todos los templates de esta carpeta se referencian desde `auth_routes.py` usando la ruta `MiloAdmin/nombre_template.html`:

```python
return render_template('MiloAdmin/admin_users.html', users=users, roles=roles, search_form=search_form, config=load_app_config())
```

## Características del Sistema MiloAdmin

- ✅ Lista completa de usuarios con paginación
- ✅ Búsqueda y filtrado de usuarios
- ✅ Gestión de roles y permisos
- ✅ Edición de perfiles de usuario
- ✅ Activación/desactivación de cuentas
- ✅ Verificación de usuarios
- ✅ Auditoría de acciones administrativas

## Permisos Requeridos

Todos los endpoints administrativos requieren:

- Usuario autenticado (`@login_required`)
- Rol de administrador (`@admin_required`)
- Permisos específicos según la acción (`@permission_required`)

## Acceso

Para acceder al panel administrativo:

- Iniciar sesión con credenciales de administrador
- Navegar a `/auth/admin/users`
- Usar las herramientas de gestión disponibles
