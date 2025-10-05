"""
MiloApps - Servicio de Email
Configuración y funciones para envío de emails con Gmail SMTP
"""

from flask import current_app, render_template, url_for
from flask_mail import Mail, Message
import os
from datetime import datetime

mail = Mail()

def init_mail(app):
    """Inicializa el servicio de email"""
    # Configuración Gmail SMTP
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    
    # Configuración desde variables de entorno
    app.config['MAIL_USERNAME'] = os.environ.get('GMAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('GMAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('GMAIL_USERNAME')
    
    # Configuración de la aplicación
    app.config['MAIL_SUBJECT_PREFIX'] = '[MiloApps] '
    app.config['INFOMILO_ADMIN'] = os.environ.get('INFOMILO_ADMIN', app.config['MAIL_USERNAME'])
    
    mail.init_app(app)
    
    # Verificar configuración
    if not app.config['MAIL_USERNAME']:
        print("⚠️  GMAIL_USERNAME no configurado en variables de entorno")
    if not app.config['MAIL_PASSWORD']:
        print("⚠️  GMAIL_PASSWORD no configurado en variables de entorno")
    else:
        print("✅ Servicio de email configurado con Gmail SMTP")

def send_email(to, subject, template, **kwargs):
    """
    Envía un email usando una plantilla HTML
    
    Args:
        to: Email del destinatario
        subject: Asunto del email
        template: Nombre de la plantilla HTML (sin extensión)
        **kwargs: Variables para la plantilla
    """
    try:
        app = current_app._get_current_object()
        
        msg = Message(
            subject=app.config['MAIL_SUBJECT_PREFIX'] + subject,
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[to]
        )
        
        # Renderizar plantilla HTML
        msg.html = render_template(f'email/{template}.html', **kwargs)
        
        # Renderizar plantilla de texto plano (opcional)
        try:
            msg.body = render_template(f'email/{template}.txt', **kwargs)
        except:
            # Si no existe plantilla .txt, crear versión básica
            msg.body = f"InfoMilo - {subject}\n\n"
            msg.body += "Este es un email de InfoMilo. Por favor, usa un cliente de email que soporte HTML para ver el contenido completo.\n\n"
            msg.body += "Si tienes problemas, contacta con el administrador."
        
        mail.send(msg)
        return True
        
    except Exception as e:
        print(f"❌ Error enviando email a {to}: {e}")
        return False

def send_password_reset_email(user):
    """Envía email de recuperación de contraseña"""
    token = user.generate_reset_token()
    
    # Generar URL de reset
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    
    return send_email(
        to=user.email,
        subject='Recuperación de contraseña',
        template='password_reset',
        user=user,
        reset_url=reset_url,
        token=token,
        expires_in_minutes=60
    )

def send_welcome_email(user, temp_password=None):
    """Envía email de bienvenida a nuevo usuario"""
    login_url = url_for('auth.login', _external=True)
    
    return send_email(
        to=user.email,
        subject='Bienvenido a MiloApps',
        template='welcome',
        user=user,
        login_url=login_url,
        temp_password=temp_password,
        company_name="MiloApps"
    )

def send_password_changed_email(user):
    """Envía email de confirmación de cambio de contraseña"""
    return send_email(
        to=user.email,
        subject='Contraseña cambiada exitosamente',
        template='password_changed',
        user=user,
        changed_at=datetime.utcnow()
    )

def send_account_locked_email(user):
    """Envía email de notificación de cuenta bloqueada"""
    return send_email(
        to=user.email,
        subject='Cuenta bloqueada temporalmente',
        template='account_locked',
        user=user,
        unlock_time=user.locked_until,
        support_email=current_app.config['INFOMILO_ADMIN']
    )

def send_two_factor_enabled_email(user):
    """Envía email de confirmación de 2FA activado"""
    return send_email(
        to=user.email,
        subject='Autenticación de dos factores activada',
        template='two_factor_enabled',
        user=user,
        enabled_at=datetime.utcnow()
    )

def send_login_alert_email(user, ip_address, location=None, browser=None):
    """Envía email de alerta de nuevo inicio de sesión"""
    return send_email(
        to=user.email,
        subject='Nuevo inicio de sesión detectado',
        template='login_alert',
        user=user,
        ip_address=ip_address,
        location=location,
        browser=browser,
        login_time=datetime.utcnow()
    )

def send_security_alert_email(user, event_type, details):
    """Envía email de alerta de seguridad"""
    return send_email(
        to=user.email,
        subject='Alerta de seguridad en tu cuenta',
        template='security_alert',
        user=user,
        event_type=event_type,
        details=details,
        alert_time=datetime.utcnow(),
        support_email=current_app.config['INFOMILO_ADMIN']
    )

def send_admin_notification_email(subject, message, details=None):
    """Envía notificación al administrador"""
    admin_email = current_app.config['INFOMILO_ADMIN']
    
    if not admin_email:
        print("⚠️  No hay email de administrador configurado")
        return False
    
    return send_email(
        to=admin_email,
        subject=f'Notificación Admin: {subject}',
        template='admin_notification',
        message=message,
        details=details,
        timestamp=datetime.utcnow()
    )

def test_email_configuration():
    """Prueba la configuración de email"""
    try:
        app = current_app._get_current_object()
        
        # Verificar variables de entorno
        if not app.config.get('MAIL_USERNAME'):
            return False, "GMAIL_USERNAME no configurado"
        
        if not app.config.get('MAIL_PASSWORD'):
            return False, "GMAIL_PASSWORD no configurado"
        
        # Intentar enviar email de prueba
        test_email = app.config['MAIL_USERNAME']
        
        msg = Message(
            subject='[InfoMilo] Prueba de configuración de email',
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[test_email]
        )
        
        msg.body = f"""
InfoMilo - Prueba de Email

Este es un email de prueba para verificar la configuración de Gmail SMTP.

Configuración actual:
- Servidor: {app.config['MAIL_SERVER']}
- Puerto: {app.config['MAIL_PORT']}
- Usuario: {app.config['MAIL_USERNAME']}
- Fecha: {datetime.utcnow()}

Si recibes este email, la configuración es correcta.

Saludos,
Sistema InfoMilo
        """
        
        mail.send(msg)
        return True, "Email de prueba enviado exitosamente"
        
    except Exception as e:
        return False, f"Error en configuración: {str(e)}"

# Decorador para funciones que requieren email
def email_required(func):
    """Decorador que verifica si el email está configurado"""
    def wrapper(*args, **kwargs):
        if not current_app.config.get('MAIL_USERNAME'):
            print("⚠️  Email no configurado - función omitida")
            return False
        return func(*args, **kwargs)
    return wrapper

# Plantillas de email por defecto (para casos donde no hay archivo)
DEFAULT_EMAIL_TEMPLATES = {
    'password_reset': {
        'subject': 'Recuperación de contraseña',
        'body': '''
Hola {user_name},

Has solicitado recuperar tu contraseña de InfoMilo.

Para establecer una nueva contraseña, haz clic en el siguiente enlace:
{reset_url}

Este enlace expira en 60 minutos.

Si no solicitaste este cambio, ignora este email.

Saludos,
Equipo InfoMilo
        '''
    },
    'welcome': {
        'subject': 'Bienvenido a InfoMilo',
        'body': '''
¡Bienvenido a InfoMilo, {user_name}!

Tu cuenta ha sido creada exitosamente.

Detalles de tu cuenta:
- Email: {user_email}
- Usuario: {user_username}
{temp_password_info}

Puedes iniciar sesión en: {login_url}

¡Gracias por unirte a InfoMilo!

Saludos,
Equipo InfoMilo
        '''
    }
}

def send_simple_email(to, subject, body):
    """Envía email simple sin plantilla"""
    try:
        app = current_app._get_current_object()
        
        msg = Message(
            subject=app.config['MAIL_SUBJECT_PREFIX'] + subject,
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[to],
            body=body
        )
        
        mail.send(msg)
        return True
        
    except Exception as e:
        print(f"❌ Error enviando email simple a {to}: {e}")
        return False
