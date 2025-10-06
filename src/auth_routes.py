"""
MiloApps - Rutas de Autenticación
Blueprint para login, registro, recuperación y gestión de usuarios
"""

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    jsonify,
    session,
    current_app,
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
    fresh_login_required,
)
from urllib.parse import urlparse
from datetime import datetime
import secrets
import json
import os

from models import (
    User,
    Role,
    Application,
    Functionality,
    RoleAppAccess,
    RoleFunctionality,
    UserRole,
    db,
    log_audit_event,
    AuditEvents,
)
from forms import (
    LoginForm,
    RegisterForm,
    ForgotPasswordForm,
    ResetPasswordForm,
    ChangePasswordForm,
    ProfileForm,
    TwoFactorSetupForm,
    TwoFactorDisableForm,
    UserManagementForm,
    SearchForm,
    RoleForm,
    ApplicationForm,
    FunctionalityForm,
    AssignUserRolesForm,
)
from email_service import (
    send_password_reset_email,
    send_welcome_email,
    send_password_changed_email,
    send_account_locked_email,
    send_two_factor_enabled_email,
    send_login_alert_email,
)
from decorators import admin_required
from utils import get_client_info, is_suspicious_login


def load_app_config():
    """Cargar configuración personalizada de la aplicación"""
    try:
        # Intentar cargar configuración activa
        config_path = os.path.join(
            os.path.dirname(__file__), "..", "config", "active.json"
        )
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass

    # Cargar configuración por defecto
    try:
        default_path = os.path.join(
            os.path.dirname(__file__), "..", "config", "default.json"
        )
        with open(default_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        pass

    return {"environment": "unknown", "description": "Configuración no disponible"}


# Crear Blueprint
auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Página de inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            # Verificar si la cuenta está bloqueada
            if user.is_locked():
                flash(
                    "Tu cuenta está temporalmente bloqueada. Intenta más tarde.",
                    "danger",
                )
                log_audit_event(
                    user.id,
                    AuditEvents.LOGIN_FAILED,
                    "Intento de login con cuenta bloqueada",
                    request=request,
                )
                return render_template(
                    "MiloAuth/login.html", form=form, config=load_app_config()
                )

            # Verificar si la cuenta está activa
            if not user.is_active:
                flash(
                    "Tu cuenta está desactivada. Contacta al administrador.", "danger"
                )
                log_audit_event(
                    user.id,
                    AuditEvents.LOGIN_FAILED,
                    "Intento de login con cuenta desactivada",
                    request=request,
                )
                return render_template(
                    "MiloAuth/login.html", form=form, config=load_app_config()
                )

            # Verificar 2FA si está habilitado
            if user.two_factor_enabled:
                if not form.two_factor_token.data:
                    flash(
                        "Se requiere código de autenticación de dos factores.",
                        "warning",
                    )
                    return render_template(
                        "MiloAuth/login.html",
                        form=form,
                        show_2fa=True,
                        config=load_app_config(),
                    )

                if not user.verify_2fa_token(form.two_factor_token.data):
                    user.increment_failed_login()
                    db.session.commit()
                    flash("Código de 2FA inválido.", "danger")
                    log_audit_event(
                        user.id,
                        AuditEvents.LOGIN_FAILED,
                        "Código 2FA inválido",
                        request=request,
                    )
                    return render_template(
                        "MiloAuth/login.html",
                        form=form,
                        show_2fa=True,
                        config=load_app_config(),
                    )

            # 🔐 CONTROL DE SESIÓN ÚNICA - Login exitoso
            user.reset_failed_login()

            # Generar nuevo session_id para sesión única
            new_session_id = secrets.token_urlsafe(32)
            client_info = get_client_info(request)

            # Iniciar nueva sesión (desplaza la anterior automáticamente)
            user.start_session(
                new_session_id, request.remote_addr, client_info.get("user_agent", "")
            )

            db.session.commit()

            # Configurar sesión Flask
            login_user(user, remember=form.remember_me.data)
            session.permanent = True
            session["session_id"] = new_session_id
            session["session_start"] = datetime.utcnow().isoformat()

            # Log de auditoría
            client_info = get_client_info(request)
            log_audit_event(
                user.id,
                AuditEvents.LOGIN_SUCCESS,
                f'Login exitoso desde {client_info["browser"]}',
                request=request,
                additional_data=client_info,
            )

            # Verificar login sospechoso
            if is_suspicious_login(user, request):
                send_login_alert_email(
                    user,
                    request.remote_addr,
                    client_info.get("location"),
                    client_info.get("browser"),
                )

            flash(f"¡Bienvenido, {user.first_name}!", "success")

            # Redireccionar a página solicitada o dashboard
            next_page = request.args.get("next")
            if not next_page or urlparse(next_page).netloc != "":
                next_page = url_for("dashboard")

            return redirect(next_page)

        else:
            # Login fallido
            if user:
                user.increment_failed_login()
                db.session.commit()

                if user.is_locked():
                    send_account_locked_email(user)
                    flash(
                        (
                            "Demasiados intentos fallidos. "
                            "Tu cuenta ha sido bloqueada temporalmente."
                        ),
                        "danger",
                    )
                else:
                    remaining = 3 - user.failed_login_attempts
                    flash(
                        (
                            "Email o contraseña incorrectos. "
                            f"Te quedan {remaining} intentos."
                        ),
                        "danger",
                    )

                log_audit_event(
                    user.id,
                    AuditEvents.LOGIN_FAILED,
                    "Contraseña incorrecta",
                    request=request,
                )
            else:
                flash("Email o contraseña incorrectos.", "danger")
                log_audit_event(
                    None,
                    AuditEvents.LOGIN_FAILED,
                    f"Email no encontrado: {form.email.data}",
                    request=request,
                )

    return render_template("MiloAuth/login.html", form=form, config=load_app_config())


@auth.route("/logout")
@login_required
def logout():
    """Cerrar sesión"""
    log_audit_event(
        current_user.id, AuditEvents.LOGOUT, "Usuario cerró sesión", request=request
    )

    logout_user()
    flash("Has cerrado sesión exitosamente.", "info")
    return redirect(url_for("index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    """Página de registro de usuario"""
    # Verificar si el registro está habilitado
    if not current_app.config.get("REGISTRATION_ENABLED", True):
        flash("El registro de nuevos usuarios está deshabilitado.", "warning")
        return redirect(url_for("auth.login"))

    form = RegisterForm()

    if form.validate_on_submit():
        # Obtener rol por defecto
        default_role = Role.query.filter_by(name="user").first()
        if form.role.data and current_user.is_authenticated and current_user.is_admin():
            selected_role = Role.query.get(form.role.data)
            if selected_role:
                default_role = selected_role

        # Crear nuevo usuario
        user = User(
            email=form.email.data.lower(),
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            company=form.company.data,
            department=form.department.data,
            role_id=default_role.id if default_role else None,
            is_active=True,
            is_verified=False,  # Requiere verificación por email
        )
        user.set_password(form.password.data)

        try:
            db.session.add(user)
            db.session.commit()

            # Log de auditoría
            log_audit_event(
                user.id,
                AuditEvents.USER_CREATED,
                f"Usuario registrado: {user.email}",
                request=request,
            )

            # Enviar email de bienvenida
            send_welcome_email(user)

            flash(
                "¡Registro exitoso! Revisa tu email para activar tu cuenta.", "success"
            )
            return redirect(url_for("auth.login"))

        except Exception as e:
            db.session.rollback()
            flash("Error al crear la cuenta. Intenta nuevamente.", "danger")
            current_app.logger.error(f"Error en registro: {e}")

    return render_template(
        "MiloAuth/register.html", form=form, config=load_app_config()
    )


@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """Página de recuperación de contraseña"""
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            # Generar token de reset (guardado en el usuario)
            user.generate_reset_token()
            db.session.commit()

            # Enviar email
            if send_password_reset_email(user):
                flash("Se ha enviado un enlace de recuperación a tu email.", "info")
                log_audit_event(
                    user.id,
                    AuditEvents.PASSWORD_RESET_REQUEST,
                    "Solicitud de reset de contraseña",
                    request=request,
                )
            else:
                flash("Error al enviar el email. Intenta más tarde.", "danger")
        else:
            # Por seguridad, mostrar el mismo mensaje aunque el email no exista
            flash("Se ha enviado un enlace de recuperación a tu email.", "info")

        return redirect(url_for("auth.login"))

    return render_template(
        "MiloAuth/forgot_password.html", form=form, config=load_app_config()
    )


@auth.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """Página de restablecimiento de contraseña"""
    user = User.query.filter_by(reset_token=token).first()

    if not user or not user.verify_reset_token(token):
        flash("El enlace de recuperación es inválido o ha expirado.", "danger")
        return redirect(url_for("auth.forgot_password"))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.clear_reset_token()
        user.unlock_account()  # Desbloquear si estaba bloqueada
        db.session.commit()

        # Enviar confirmación por email
        send_password_changed_email(user)

        # Log de auditoría
        log_audit_event(
            user.id,
            AuditEvents.PASSWORD_RESET_SUCCESS,
            "Contraseña restablecida via email",
            request=request,
        )

        flash("Tu contraseña ha sido actualizada exitosamente.", "success")
        return redirect(url_for("auth.login"))

    return render_template(
        "MiloAuth/forgot_password.html",
        form=form,
        show_reset_form=True,
        token=token,
        config=load_app_config(),
    )


@auth.route("/upload-profile-picture", methods=["POST"])
@login_required
def upload_profile_picture():
    """Subir foto de perfil"""
    import os
    import secrets
    from werkzeug.utils import secure_filename
    from PIL import Image
    
    if 'profile_picture' not in request.files:
        return jsonify({'success': False, 'message': 'No se seleccionó archivo'})
    
    file = request.files['profile_picture']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No se seleccionó archivo'})
    
    # Validar tipo de archivo
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({'success': False, 'message': 'Tipo de archivo no permitido'})
    
    # Validar tamaño (max 5MB)
    if len(file.read()) > 5 * 1024 * 1024:
        return jsonify({'success': False, 'message': 'Archivo muy grande (max 5MB)'})
    file.seek(0)
    
    try:
        # Generar nombre único
        filename = secrets.token_hex(16) + '.' + file.filename.rsplit('.', 1)[1].lower()
        
        # Crear directorio si no existe
        upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'profiles')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Guardar archivo temporal
        filepath = os.path.join(upload_dir, filename)
        file.save(filepath)
        
        # Redimensionar imagen
        with Image.open(filepath) as img:
            img = img.convert('RGB')
            # Redimensionar manteniendo proporción, max 300x300
            img.thumbnail((300, 300), Image.Resampling.LANCZOS)
            img.save(filepath, 'JPEG', quality=90)
        
        # Eliminar foto anterior si existe
        if current_user.profile_picture:
            old_path = os.path.join(upload_dir, current_user.profile_picture)
            if os.path.exists(old_path):
                os.remove(old_path)
        
        # Actualizar usuario
        current_user.profile_picture = filename
        db.session.commit()
        
        # Log de auditoría
        log_audit_event(
            current_user.id,
            AuditEvents.PROFILE_UPDATE,
            "Foto de perfil actualizada",
            request=request,
        )
        
        return jsonify({
            'success': True, 
            'message': 'Foto de perfil actualizada exitosamente',
            'profile_picture_url': current_user.get_profile_picture_url()
        })
        
    except Exception as e:
        current_app.logger.error(f"Error subiendo foto: {e}")
        return jsonify({'success': False, 'message': 'Error al subir la foto'})


@auth.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Página de perfil de usuario"""
    form = ProfileForm(
        original_username=current_user.username, original_email=current_user.email
    )

    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data.lower()
        current_user.phone = form.phone.data
        current_user.company = form.company.data
        current_user.department = form.department.data
        current_user.bio = form.bio.data

        try:
            db.session.commit()

            log_audit_event(
                current_user.id,
                AuditEvents.PROFILE_UPDATE,
                "Perfil actualizado",
                request=request,
            )

            flash("Tu perfil ha sido actualizado exitosamente.", "success")
            return redirect(url_for("auth.profile"))

        except Exception as e:
            db.session.rollback()
            flash("Error al actualizar el perfil.", "danger")
            current_app.logger.error(f"Error actualizando perfil: {e}")

    elif request.method == "GET":
        # Cargar datos actuales en el formulario
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.company.data = current_user.company
        form.department.data = current_user.department
        form.bio.data = current_user.bio

    return render_template("MiloAuth/profile.html", form=form, config=load_app_config())


@auth.route("/change-password", methods=["GET", "POST"])
@fresh_login_required
def change_password():
    """Página de cambio de contraseña"""
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()

            # Enviar confirmación por email
            send_password_changed_email(current_user)

            # Log de auditoría
            log_audit_event(
                current_user.id,
                AuditEvents.PASSWORD_CHANGE,
                "Contraseña cambiada por el usuario",
                request=request,
            )

            flash("Tu contraseña ha sido cambiada exitosamente.", "success")
            return redirect(url_for("auth.profile"))
        else:
            flash("La contraseña actual es incorrecta.", "danger")

    return render_template(
        "MiloAuth/change_password.html", form=form, config=load_app_config()
    )


@auth.route("/two-factor")
@login_required
def two_factor():
    """Página de gestión de autenticación de dos factores"""
    return render_template("MiloAuth/two_factor.html", config=load_app_config())


@auth.route("/two-factor/setup", methods=["GET", "POST"])
@fresh_login_required
def two_factor_setup():
    """Configurar autenticación de dos factores"""
    if current_user.two_factor_enabled:
        flash("La autenticación de dos factores ya está habilitada.", "info")
        return redirect(url_for("auth.two_factor"))

    form = TwoFactorSetupForm()

    # Generar secreto si no existe
    secret = current_user.generate_2fa_secret()
    qr_code = current_user.get_2fa_qr_code()

    if form.validate_on_submit():
        if current_user.verify_2fa_token(form.token.data):
            current_user.two_factor_enabled = True
            db.session.commit()

            # Enviar confirmación por email
            send_two_factor_enabled_email(current_user)

            # Log de auditoría
            log_audit_event(
                current_user.id,
                AuditEvents.TWO_FACTOR_ENABLED,
                "Autenticación de dos factores habilitada",
                request=request,
            )

            flash("¡Autenticación de dos factores habilitada exitosamente!", "success")
            return redirect(url_for("auth.two_factor"))
        else:
            flash("Código inválido. Intenta nuevamente.", "danger")

    return render_template(
        "MiloAuth/two_factor_setup.html",
        form=form,
        secret=secret,
        qr_code=qr_code,
        config=load_app_config(),
    )


@auth.route("/two-factor/disable", methods=["GET", "POST"])
@fresh_login_required
def two_factor_disable():
    """Desactivar autenticación de dos factores"""
    if not current_user.two_factor_enabled:
        flash("La autenticación de dos factores no está habilitada.", "info")
        return redirect(url_for("auth.two_factor"))

    form = TwoFactorDisableForm()

    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            current_user.two_factor_enabled = False
            current_user.two_factor_secret = None
            db.session.commit()

            # Log de auditoría
            log_audit_event(
                current_user.id,
                AuditEvents.TWO_FACTOR_DISABLED,
                "Autenticación de dos factores deshabilitada",
                request=request,
            )

            flash("Autenticación de dos factores deshabilitada.", "warning")
            return redirect(url_for("auth.two_factor"))
        else:
            flash("Contraseña incorrecta.", "danger")

    return render_template(
        "MiloAuth/two_factor_disable.html", form=form, config=load_app_config()
    )


# Rutas de administración
@auth.route("/admin/users")
@login_required
@admin_required
def admin_users():
    """Panel de administración de usuarios"""
    search_form = SearchForm()
    page = request.args.get("page", 1, type=int)

    query = User.query

    # Aplicar filtros de búsqueda
    search_query = request.args.get("query") or request.args.get("q")
    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(
            db.or_(
                User.email.like(search_term),
                User.username.like(search_term),
                User.first_name.like(search_term),
                User.last_name.like(search_term),
                User.company.like(search_term),
            )
        )

    # Filtros adicionales
    if request.args.get("role"):
        query = query.filter(User.role_id == request.args.get("role"))

    if request.args.get("status") == "active":
        query = query.filter(User.is_active.is_(True))
    elif request.args.get("status") == "inactive":
        query = query.filter(User.is_active.is_(False))
    elif request.args.get("status") == "locked":
        query = query.filter(User.locked_until.isnot(None))

    # Paginación
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    roles = Role.query.filter_by(is_active=True).all()

    return render_template(
        "MiloAdmin/admin_users.html",
        users=users,
        roles=roles,
        search_form=search_form,
        config=load_app_config(),
    )


@auth.route("/admin/users/<int:user_id>", methods=["GET", "POST"])
@login_required
@admin_required
def admin_user_detail(user_id):
    """Detalle y edición de usuario (solo admin)"""
    user = User.query.get_or_404(user_id)
    form = UserManagementForm()
    assign_roles_form = AssignUserRolesForm()

    if form.validate_on_submit() and request.form.get("form_name") == "user_management":
        # Actualizar datos básicos
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.username = form.username.data
        user.email = form.email.data.lower()
        user.phone = form.phone.data
        user.company = form.company.data
        user.department = form.department.data
        user.role_id = form.role.data
        user.is_active = form.is_active.data
        user.is_verified = form.is_verified.data

        # Acciones especiales
        if form.unlock_account.data:
            user.unlock_account()

        if form.disable_2fa.data:
            user.two_factor_enabled = False
            user.two_factor_secret = None

        if form.reset_password.data:
            temp_password = secrets.token_urlsafe(12)
            user.set_password(temp_password)
            # Enviar nueva contraseña por email
            send_welcome_email(user, temp_password)

        try:
            db.session.commit()

            log_audit_event(current_user.id, AuditEvents.USER_UPDATED,
                            f"Usuario {user.email} actualizado por admin",
                            request=request, resource_type="user",
                            resource_id=str(user.id))

            flash("Usuario actualizado exitosamente.", "success")
            return redirect(url_for("auth.admin_user_detail", user_id=user.id))

        except Exception as e:
            db.session.rollback()
            flash("Error al actualizar el usuario.", "danger")
            current_app.logger.error(f"Error actualizando usuario: {e}")

    elif request.method == "GET":
        # Cargar datos actuales
        form.user_id.data = user.id
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.username.data = user.username
        form.email.data = user.email
        form.phone.data = user.phone
        form.company.data = user.company
        form.department.data = user.department
        form.role.data = user.role_id
        form.is_active.data = user.is_active
    form.is_verified.data = user.is_verified
    # Inicializar formulario de roles adicionales
    current_role_ids = {r.id for r in user.roles}
    assign_roles_form.roles.data = list(current_role_ids)

    return render_template(
        "MiloAdmin/admin_user_detail.html",
        user=user,
        form=form,
        assign_roles_form=assign_roles_form,
        config=load_app_config(),
    )


@auth.route("/admin/users/<int:user_id>/assign-roles", methods=["POST"])
@login_required
@admin_required
def admin_assign_user_roles(user_id):
    """Asignar múltiples roles adicionales a un usuario."""
    user = User.query.get_or_404(user_id)
    form = AssignUserRolesForm()
    if form.validate_on_submit():
        try:
            # Limpiar roles actuales adicionales (no tocar rol primario role_id)
            UserRole.query.filter_by(user_id=user.id).delete()
            db.session.flush()

            for role_id in form.roles.data:
                db.session.add(UserRole(user_id=user.id, role_id=role_id))

            db.session.commit()
            flash("Roles adicionales actualizados.", "success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error asignando roles: {e}")
            flash("Error al actualizar los roles.", "danger")

    return redirect(url_for("auth.admin_user_detail", user_id=user.id))


# ===== Administración de Roles =====
@auth.route("/admin/roles", methods=["GET", "POST"])
@login_required
@admin_required
def admin_roles():
    form = RoleForm()
    if form.validate_on_submit():
        try:
            role = Role(
                name=form.name.data.strip(),
                display_name=form.display_name.data.strip(),
                description=form.description.data,
                is_allmilo=form.is_allmilo.data,
                is_active=form.is_active.data,
            )
            db.session.add(role)
            db.session.commit()
            flash("Rol creado correctamente.", "success")
            return redirect(url_for("auth.admin_roles"))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creando rol: {e}")
            flash("Error al crear el rol.", "danger")

    roles = Role.query.order_by(Role.display_name.asc()).all()
    return render_template(
        "MiloAdmin/admin_roles.html", form=form, roles=roles, config=load_app_config()
    )


@auth.route("/admin/roles/<int:role_id>/permissions", methods=["GET", "POST"])
@login_required
@admin_required
def admin_role_permissions(role_id):
    role = Role.query.get_or_404(role_id)
    apps = Application.query.order_by(Application.name.asc()).all()

    if request.method == "POST":
        try:
            # Limpiar permisos previos
            RoleAppAccess.query.filter_by(role_id=role.id).delete()
            RoleFunctionality.query.filter_by(role_id=role.id).delete()
            db.session.flush()

            for app in apps:
                full_flag = request.form.get(f"full_access_{app.id}") == "on"
                if full_flag:
                    db.session.add(
                        RoleAppAccess(role_id=role.id, app_id=app.id, full_access=True)
                    )
                # funcionalidades
                for func in app.functionalities:
                    key = f"func_{app.id}_{func.id}"
                    if request.form.get(key) == "on":
                        db.session.add(
                            RoleFunctionality(role_id=role.id, functionality_id=func.id)
                        )

            db.session.commit()
            flash("Permisos actualizados.", "success")
            return redirect(url_for("auth.admin_role_permissions", role_id=role.id))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error guardando permisos de rol: {e}")
            flash("Error al guardar permisos.", "danger")

    # Construir estado actual
    full_access_map = {
        a.app_id: a
        for a in RoleAppAccess.query.filter_by(role_id=role.id).all()
        if a.full_access
    }
    func_ids = {
        rf.functionality_id
        for rf in RoleFunctionality.query.filter_by(role_id=role.id).all()
    }

    return render_template(
        "MiloAdmin/admin_role_permissions.html",
        role=role,
        apps=apps,
        full_access_map=full_access_map,
        func_ids=func_ids,
        config=load_app_config(),
    )


# ===== Administración de Aplicaciones =====
@auth.route("/admin/apps", methods=["GET", "POST"])
@login_required
@admin_required
def admin_apps():
    form = ApplicationForm()
    if form.validate_on_submit():
        try:
            app = Application(
                key=form.key.data.strip(),
                name=form.name.data.strip(),
                description=form.description.data,
                is_active=form.is_active.data,
            )
            db.session.add(app)
            db.session.commit()
            flash("Aplicación creada.", "success")
            return redirect(url_for("auth.admin_apps"))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creando aplicación: {e}")
            flash("Error al crear la aplicación.", "danger")

    apps = Application.query.order_by(Application.created_at.desc()).all()
    return render_template(
        "MiloAdmin/admin_apps.html", form=form, apps=apps, config=load_app_config()
    )


@auth.route("/admin/functionalities", methods=["GET", "POST"])
@login_required
@admin_required
def admin_functionalities():
    form = FunctionalityForm()
    if form.validate_on_submit():
        try:
            func = Functionality(
                application_id=form.app_id.data,
                key=form.key.data.strip(),
                name=form.name.data.strip(),
                description=form.description.data,
                is_active=form.is_active.data,
            )
            db.session.add(func)
            db.session.commit()
            flash("Funcionalidad creada.", "success")
            return redirect(url_for("auth.admin_functionalities"))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creando funcionalidad: {e}")
            flash("Error al crear la funcionalidad.", "danger")

    # Listado por aplicación
    apps = Application.query.order_by(Application.name.asc()).all()
    return render_template(
        "MiloAdmin/admin_functionalities.html",
        form=form,
        apps=apps,
        config=load_app_config(),
    )


# Rutas API para AJAX
@auth.route("/api/check-email")
def api_check_email():
    """API para verificar si un email ya existe"""
    email = request.args.get("email")
    if email:
        exists = User.query.filter_by(email=email.lower()).first() is not None
        return jsonify({"exists": exists})
    return jsonify({"exists": False})


@auth.route("/api/check-username")
def api_check_username():
    """API para verificar si un username ya existe"""
    username = request.args.get("username")
    if username:
        exists = User.query.filter_by(username=username).first() is not None
        return jsonify({"exists": exists})
    return jsonify({"exists": False})
