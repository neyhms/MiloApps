# MiloMail - Templates de Correo Electrónico

Esta carpeta contiene todos los templates HTML para el sistema de correo electrónico de MiloApps.

## Estructura de Archivos

### Templates de Email Disponibles

- `welcome.html` - Email de bienvenida para nuevos usuarios
- `password_reset.html` - Email para recuperación de contraseña
- `password_changed.html` - Notificación de cambio de contraseña
- `account_locked.html` - Notificación de cuenta bloqueada
- `two_factor_enabled.html` - Confirmación de 2FA activado
- `login_alert.html` - Alertas de inicio de sesión sospechoso
- `security_alert.html` - Alertas generales de seguridad
- `admin_notification.html` - Notificaciones administrativas

## Uso en el Sistema

Los templates se utilizan desde `email_service.py` usando la nueva estructura:

```python
msg.html = render_template(f'MiloMail/{template}.html', **kwargs)
msg.body = render_template(f'MiloMail/{template}.txt', **kwargs)  # opcional
```

## Funciones de Email Asociadas

### Emails de Autenticación

- `send_welcome_email()` - Usa `welcome.html`
- `send_password_reset_email()` - Usa `password_reset.html`
- `send_password_changed_email()` - Usa `password_changed.html`

### Emails Administrativos

- `send_account_locked_email()` - Notificación de cuenta bloqueada
- `send_two_factor_enabled_email()` - Confirmación de 2FA activado
- `send_login_alert_email()` - Alertas de inicio de sesión sospechoso

## Características de los Templates

- ✅ **Diseño Responsive**: Compatible con todos los clientes de email
- ✅ **Branding Consistente**: Colores y logos de MiloApps
- ✅ **HTML/Text**: Soporte para versiones HTML y texto plano
- ✅ **Variables Dinámicas**: Personalización con datos del usuario
- ✅ **Enlaces Seguros**: URLs con tokens de seguridad
- ✅ **Compatibilidad**: Funciona en Gmail, Outlook, Apple Mail, etc.

## Configuración SMTP

Los emails se envían usando la configuración en:

- `MAIL_SERVER`: Servidor SMTP
- `MAIL_PORT`: Puerto (587 para TLS)
- `MAIL_USE_TLS`: Encriptación
- `MAIL_USERNAME`: Usuario SMTP
- `MAIL_PASSWORD`: Contraseña SMTP

## Variables Disponibles en Templates

### Variables Comunes

- `user` - Objeto usuario completo
- `app_name` - Nombre de la aplicación
- `contact_email` - Email de contacto
- `base_url` - URL base de la aplicación

### Variables Específicas

- **welcome.html**: `temp_password` (si aplica)
- **password_reset.html**: `reset_url`, `token`
- **password_changed.html**: `change_time`, `ip_address`

## Personalización

Para personalizar los emails:

1. Editar los templates HTML en esta carpeta
2. Mantener la estructura de variables existentes
3. Probar con `email_test.html` antes de usar en producción
4. Considerar versiones de texto plano (.txt) para mejor compatibilidad

## Testing

Usar la función de prueba para validar templates:

```python
test_email_template('welcome', user=test_user)
```
