# Core MiloApps - Utilidades compartidas
from flask import request, session, current_app
from functools import wraps
from .models import AuditLog, User, UserAppPermission, db
import json
from datetime import datetime
from user_agents import parse


def log_audit(
    action, app_name, user_id=None, resource_type=None, resource_id=None, details=None
):
    """Registrar acción en el log de auditoría"""
    try:
        # Obtener información de la request
        ip_address = request.remote_addr if request else None
        user_agent = request.headers.get("User-Agent") if request else None

        # Crear entrada de auditoría
        audit_entry = AuditLog(
            user_id=user_id,
            app_name=app_name,
            action=action,
            resource_type=resource_type,
            resource_id=str(resource_id) if resource_id else None,
            details=json.dumps(details) if details else None,
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=datetime.utcnow(),
        )

        db.session.add(audit_entry)
        db.session.commit()

        return True
    except Exception as e:
        current_app.logger.error(f"Error logging audit: {str(e)}")
        return False


def require_app_permission(app_name, required_role="user"):
    """Decorador para verificar permisos de aplicación"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask_login import current_user, login_required

            # Verificar que el usuario esté logueado
            if not current_user.is_authenticated:
                return login_required()(lambda: None)()

            # Verificar permisos de la aplicación
            if not current_user.has_app_permission(app_name):
                log_audit(
                    action="ACCESS_DENIED",
                    app_name=app_name,
                    user_id=current_user.id,
                    details={"reason": "No app permission", "required_app": app_name},
                )
                return {
                    "error": "No tienes permisos para acceder a esta aplicación"
                }, 403

            # Verificar rol si es necesario
            if required_role != "user":
                user_role = current_user.get_app_role(app_name)
                if not _check_role_hierarchy(user_role, required_role):
                    log_audit(
                        action="ACCESS_DENIED",
                        app_name=app_name,
                        user_id=current_user.id,
                        details={
                            "reason": "Insufficient role",
                            "required_role": required_role,
                            "user_role": user_role,
                        },
                    )
                    return {
                        "error": f"Necesitas rol de {required_role} o superior"
                    }, 403

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def _check_role_hierarchy(user_role, required_role):
    """Verificar jerarquía de roles"""
    role_hierarchy = {
        "readonly": 1,
        "user": 2,
        "moderator": 3,
        "admin": 4,
        "superadmin": 5,
    }

    user_level = role_hierarchy.get(user_role, 0)
    required_level = role_hierarchy.get(required_role, 0)

    return user_level >= required_level


def get_user_info():
    """Obtener información detallada del usuario actual"""
    from flask_login import current_user

    if not current_user.is_authenticated:
        return None

    user_agent = request.headers.get("User-Agent", "")
    parsed_ua = parse(user_agent)

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.get_full_name(),
        "is_admin": current_user.is_admin,
        "last_login": (
            current_user.last_login.isoformat() if current_user.last_login else None
        ),
        "browser_info": {
            "browser": f"{parsed_ua.browser.family} {parsed_ua.browser.version_string}",
            "os": f"{parsed_ua.os.family} {parsed_ua.os.version_string}",
            "device": parsed_ua.device.family,
            "is_mobile": parsed_ua.is_mobile,
            "is_tablet": parsed_ua.is_tablet,
            "is_pc": parsed_ua.is_pc,
        },
    }


def get_user_apps(user=None):
    """Obtener aplicaciones disponibles para el usuario"""
    from flask_login import current_user
    from .models import AppConfig

    if not user:
        user = current_user

    if not user.is_authenticated:
        return []

    # Obtener todas las aplicaciones activas
    all_apps = (
        AppConfig.query.filter_by(is_active=True).order_by(AppConfig.order_index).all()
    )

    user_apps = []
    for app in all_apps:
        # Si es admin, tiene acceso a todo
        if user.is_admin:
            user_apps.append(
                {
                    "name": app.app_name,
                    "display_name": app.display_name,
                    "description": app.description,
                    "icon": app.icon,
                    "color": app.color,
                    "url": app.url_prefix,
                    "role": "admin",
                    "has_access": True,
                }
            )
        else:
            # Verificar permisos específicos
            permission = UserAppPermission.query.filter_by(
                user_id=user.id, app_name=app.app_name, is_active=True
            ).first()

            if permission:
                user_apps.append(
                    {
                        "name": app.app_name,
                        "display_name": app.display_name,
                        "description": app.description,
                        "icon": app.icon,
                        "color": app.color,
                        "url": app.url_prefix,
                        "role": permission.role,
                        "has_access": True,
                    }
                )

    return user_apps


def detect_app_from_request():
    """Detectar qué aplicación se está accediendo basado en la URL o subdominio"""

    # Detectar por subdominio
    host = request.host.lower()
    main_domain = current_app.config.get("MILOAPPS_CONFIG", {}).get(
        "main_domain", "localhost:3000"
    )

    if current_app.config.get("MILOAPPS_CONFIG", {}).get("enable_subdomains", False):
        if host != main_domain:
            # Extraer subdominio
            subdomain = host.replace(f".{main_domain}", "").replace(
                f":{main_domain.split(':')[1]}", ""
            )
            return subdomain

    # Detectar por URL path
    path = request.path
    if path.startswith("/milosign"):
        return "milosign"
    elif path.startswith("/contratacion"):
        return "contratacion"
    elif path.startswith("/presupuesto"):
        return "presupuesto"
    elif path.startswith("/auth"):
        return "auth"

    # Default
    return "auth"


def create_user_session_data(user):
    """Crear datos de sesión para un usuario"""
    session_data = {
        "user_id": user.id,
        "username": user.username,
        "is_admin": user.is_admin,
        "apps": [app["name"] for app in get_user_apps(user)],
        "login_time": datetime.utcnow().isoformat(),
        "last_activity": datetime.utcnow().isoformat(),
    }

    # Guardar en sesión
    for key, value in session_data.items():
        session[key] = value

    return session_data


def update_user_activity():
    """Actualizar última actividad del usuario en la sesión"""
    if "user_id" in session:
        session["last_activity"] = datetime.utcnow().isoformat()
        session.permanent = True


def get_app_config(app_name):
    """Obtener configuración de una aplicación específica"""
    apps_config = current_app.config.get("APPS_CONFIG", {})
    return apps_config.get(app_name, {})


def format_datetime(dt, format_string="%Y-%m-%d %H:%M"):
    """Formatear datetime para templates"""
    if not dt:
        return ""
    return dt.strftime(format_string)


def safe_json_loads(json_string, default=None):
    """Cargar JSON de forma segura"""
    try:
        return json.loads(json_string) if json_string else default
    except (json.JSONDecodeError, TypeError):
        return default


# Funciones de template disponibles globalmente
def register_template_functions(app):
    """Registrar funciones de template globales"""

    @app.template_global()
    def get_current_user_apps():
        """Obtener apps del usuario actual para templates"""
        return get_user_apps()

    @app.template_global()
    def get_current_app_name():
        """Obtener nombre de la app actual para templates"""
        return detect_app_from_request()

    @app.template_filter()
    def datetime_format(value, format="medium"):
        """Filtro para formatear fechas en templates"""
        if format == "full":
            format = "%A, %B %d, %Y at %H:%M"
        elif format == "medium":
            format = "%B %d, %Y"
        elif format == "short":
            format = "%m/%d/%Y"
        return value.strftime(format) if value else ""

    @app.template_filter()
    def user_role_badge(role):
        """Filtro para mostrar badges de roles"""
        badges = {
            "superadmin": "badge-danger",
            "admin": "badge-primary",
            "moderator": "badge-warning",
            "user": "badge-success",
            "readonly": "badge-secondary",
        }
        return badges.get(role, "badge-secondary")
