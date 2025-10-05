# Auth App - Módulo de autenticación de MiloApps
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
try:
    from werkzeug.urls import url_parse
except ImportError:
    from urllib.parse import urlparse as url_parse
from datetime import datetime, timedelta
import pyotp
from ..core.models import User, db
from ..core.utils import log_audit, create_user_session_data, get_user_apps
from .forms import (
    LoginForm, RegistrationForm, ForgotPasswordForm, 
    ResetPasswordForm, ChangePasswordForm, ProfileForm,
    TwoFactorForm
)
from .services import EmailService

# Crear blueprint para autenticación
auth_bp = Blueprint('auth', __name__, 
                   template_folder='templates',
                   static_folder='static',
                   url_prefix='/auth')

email_service = EmailService()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            if user.is_active:
                # Verificar si el usuario está bloqueado
                if user.locked_until and user.locked_until > datetime.utcnow():
                    flash('Tu cuenta está temporalmente bloqueada. Intenta más tarde.', 'warning')
                    log_audit('LOGIN_BLOCKED', 'auth', user.id)
                    return render_template('auth/login.html', form=form)
                
                # Verificar 2FA si está habilitado
                if user.two_factor_enabled:
                    session['2fa_user_id'] = user.id
                    log_audit('2FA_REQUIRED', 'auth', user.id)
                    return redirect(url_for('auth.two_factor'))
                
                # Login exitoso
                login_user(user, remember=form.remember_me.data)
                user.last_login = datetime.utcnow()
                user.failed_login_attempts = 0
                user.locked_until = None
                db.session.commit()
                
                # Crear datos de sesión
                create_user_session_data(user)
                
                log_audit('LOGIN_SUCCESS', 'auth', user.id)
                flash(f'¡Bienvenido/a {user.get_full_name()}!', 'success')
                
                # Redirigir a la página solicitada o al dashboard
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('main.dashboard')
                return redirect(next_page)
            else:
                flash('Tu cuenta está desactivada. Contacta al administrador.', 'warning')
                log_audit('LOGIN_INACTIVE_ACCOUNT', 'auth', user.id)
        else:
            # Incrementar intentos fallidos
            if user:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 5:
                    user.locked_until = datetime.utcnow() + timedelta(minutes=30)
                    flash('Demasiados intentos fallidos. Cuenta bloqueada por 30 minutos.', 'danger')
                    log_audit('ACCOUNT_LOCKED', 'auth', user.id)
                else:
                    flash(f'Email o contraseña incorrectos. Intentos restantes: {5 - user.failed_login_attempts}', 'danger')
                    log_audit('LOGIN_FAILED', 'auth', user.id)
                db.session.commit()
            else:
                flash('Email o contraseña incorrectos.', 'danger')
                log_audit('LOGIN_FAILED_UNKNOWN_USER', 'auth', None, details={'email': form.email.data})
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/two-factor', methods=['GET', 'POST'])
def two_factor():
    """Verificación de dos factores"""
    if '2fa_user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['2fa_user_id'])
    if not user:
        session.pop('2fa_user_id', None)
        return redirect(url_for('auth.login'))
    
    form = TwoFactorForm()
    if form.validate_on_submit():
        if user.verify_2fa_token(form.token.data):
            # 2FA exitoso
            login_user(user, remember=True)
            user.last_login = datetime.utcnow()
            user.failed_login_attempts = 0
            db.session.commit()
            
            # Crear datos de sesión
            create_user_session_data(user)
            
            session.pop('2fa_user_id', None)
            log_audit('2FA_SUCCESS', 'auth', user.id)
            flash(f'¡Bienvenido/a {user.get_full_name()}!', 'success')
            
            return redirect(url_for('main.dashboard'))
        else:
            flash('Código de verificación incorrecto.', 'danger')
            log_audit('2FA_FAILED', 'auth', user.id)
    
    return render_template('auth/two_factor.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    user_id = current_user.id if current_user.is_authenticated else None
    logout_user()
    session.clear()
    log_audit('LOGOUT', 'auth', user_id)
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de nuevos usuarios"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        log_audit('USER_REGISTERED', 'auth', user.id)
        
        # Enviar email de bienvenida
        email_service.send_welcome_email(user)
        
        flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Recuperación de contraseña"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Enviar email de recuperación
            token = email_service.send_password_reset_email(user)
            log_audit('PASSWORD_RESET_REQUESTED', 'auth', user.id)
            flash('Te hemos enviado un email con las instrucciones para recuperar tu contraseña.', 'info')
        else:
            # Por seguridad, siempre mostrar el mismo mensaje
            flash('Te hemos enviado un email con las instrucciones para recuperar tu contraseña.', 'info')
            log_audit('PASSWORD_RESET_UNKNOWN_EMAIL', 'auth', None, details={'email': form.email.data})
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html', form=form)

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset de contraseña con token"""
    user = email_service.verify_reset_token(token)
    if not user:
        flash('Token inválido o expirado.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        
        log_audit('PASSWORD_RESET_COMPLETED', 'auth', user.id)
        email_service.send_password_changed_notification(user)
        
        flash('Tu contraseña ha sido actualizada correctamente.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form)

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Perfil de usuario"""
    form = ProfileForm()
    
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone = form.phone.data
        current_user.bio = form.bio.data
        
        db.session.commit()
        log_audit('PROFILE_UPDATED', 'auth', current_user.id)
        flash('Perfil actualizado correctamente.', 'success')
        return redirect(url_for('auth.profile'))
    
    # Prellenar formulario
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.phone.data = current_user.phone
    form.bio.data = current_user.bio
    
    return render_template('auth/profile.html', form=form)

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Cambiar contraseña"""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            
            log_audit('PASSWORD_CHANGED', 'auth', current_user.id)
            email_service.send_password_changed_notification(current_user)
            
            flash('Contraseña cambiada correctamente.', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Contraseña actual incorrecta.', 'danger')
    
    return render_template('auth/change_password.html', form=form)

@auth_bp.route('/setup-2fa')
@login_required
def setup_2fa():
    """Configurar autenticación de dos factores"""
    if current_user.two_factor_enabled:
        flash('Ya tienes la autenticación de dos factores habilitada.', 'info')
        return redirect(url_for('auth.profile'))
    
    # Generar secreto si no existe
    if not current_user.two_factor_secret:
        current_user.generate_2fa_secret()
        db.session.commit()
    
    qr_code = current_user.get_2fa_qr_code()
    
    return render_template('auth/two_factor_setup.html', 
                         qr_code=qr_code,
                         secret=current_user.two_factor_secret)

@auth_bp.route('/enable-2fa', methods=['POST'])
@login_required
def enable_2fa():
    """Habilitar 2FA después de verificar token"""
    token = request.form.get('token')
    
    if current_user.verify_2fa_token(token):
        current_user.two_factor_enabled = True
        db.session.commit()
        
        log_audit('2FA_ENABLED', 'auth', current_user.id)
        flash('Autenticación de dos factores habilitada correctamente.', 'success')
    else:
        flash('Código de verificación incorrecto.', 'danger')
    
    return redirect(url_for('auth.profile'))

@auth_bp.route('/disable-2fa', methods=['POST'])
@login_required
def disable_2fa():
    """Deshabilitar 2FA"""
    password = request.form.get('password')
    
    if current_user.check_password(password):
        current_user.two_factor_enabled = False
        current_user.two_factor_secret = None
        db.session.commit()
        
        log_audit('2FA_DISABLED', 'auth', current_user.id)
        flash('Autenticación de dos factores deshabilitada.', 'warning')
    else:
        flash('Contraseña incorrecta.', 'danger')
    
    return redirect(url_for('auth.profile'))

# API endpoints
@auth_bp.route('/api/user-info')
@login_required
def api_user_info():
    """API para obtener información del usuario actual"""
    from ..core.utils import get_user_info
    return jsonify(get_user_info())

@auth_bp.route('/api/user-apps')
@login_required
def api_user_apps():
    """API para obtener aplicaciones disponibles"""
    return jsonify(get_user_apps())

# Error handlers
@auth_bp.errorhandler(403)
def forbidden(error):
    return render_template('error.html', 
                         error_code=403,
                         error_message='No tienes permisos para acceder a esta página'), 403

@auth_bp.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404