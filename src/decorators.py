"""
InfoMilo - Decoradores de Seguridad
Decoradores para control de acceso y permisos
"""

from functools import wraps
from flask import abort, redirect, url_for, flash, request
from flask_login import current_user
from models import log_audit_event, AuditEvents

def admin_required(f):
    """Decorador que requiere permisos de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login', next=request.url))
        
        if not current_user.is_admin():
            flash('No tienes permisos para acceder a esta sección.', 'danger')
            log_audit_event(current_user.id, AuditEvents.PERMISSION_DENIED, 
                          f'Acceso denegado a {request.endpoint}', request=request)
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function

def permission_required(permission):
    """Decorador que requiere un permiso específico"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login', next=request.url))
            
            if not current_user.role or not current_user.role.has_permission(permission):
                flash('No tienes permisos suficientes para esta acción.', 'danger')
                log_audit_event(current_user.id, AuditEvents.PERMISSION_DENIED, 
                              f'Permiso requerido: {permission}', request=request)
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def role_required(role_name):
    """Decorador que requiere un rol específico"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login', next=request.url))
            
            if not current_user.role or current_user.role.name != role_name:
                flash(f'Se requiere rol de {role_name} para acceder.', 'danger')
                log_audit_event(current_user.id, AuditEvents.PERMISSION_DENIED, 
                              f'Rol requerido: {role_name}', request=request)
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def verified_required(f):
    """Decorador que requiere cuenta verificada"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login', next=request.url))
        
        if not current_user.is_verified:
            flash('Debes verificar tu cuenta para acceder a esta sección.', 'warning')
            return redirect(url_for('auth.profile'))
        
        return f(*args, **kwargs)
    return decorated_function

def active_required(f):
    """Decorador que requiere cuenta activa"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login', next=request.url))
        
        if not current_user.is_active:
            flash('Tu cuenta está desactivada. Contacta al administrador.', 'danger')
            return redirect(url_for('auth.logout'))
        
        return f(*args, **kwargs)
    return decorated_function

def ajax_required(f):
    """Decorador para rutas que solo aceptan peticiones AJAX"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_xhr:
            abort(400)
        return f(*args, **kwargs)
    return decorated_function
