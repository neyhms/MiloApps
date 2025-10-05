"""
MiloApps - Modelos de Base de Datos
Sistema de autenticación con usuarios, roles y auditoría
"""

from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp
import qrcode
from io import BytesIO
import base64
import secrets
import json

db = SQLAlchemy()


"""Tablas y modelos de dominio

- User mantiene role_id para compatibilidad, pero ahora soporta múltiples roles vía user_roles
- Application y Functionality permiten permisos granulares por aplicación
- Role incluye bandera is_allmilo para acceso total a todas las apps
- Mapas:
    - RoleAppAccess: acceso de rol a una app (full_access opcional)
    - RoleFunctionality: permisos granulares por funcionalidad
    - UserRole: asignación de múltiples roles al usuario
"""


class User(UserMixin, db.Model):
    """Modelo de Usuario con autenticación completa"""

    __tablename__ = "users"

    # Campos principales
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Información personal
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    company = db.Column(db.String(100), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)  # Biografía del usuario

    # Rol y permisos
    # Mantener role_id para compatibilidad con plantillas existentes (rol primario)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)

    # Autenticación de dos factores
    two_factor_enabled = db.Column(db.Boolean, default=False, nullable=False)
    two_factor_secret = db.Column(db.String(32), nullable=True)

    # Control de acceso
    failed_login_attempts = db.Column(db.Integer, default=0, nullable=False)
    locked_until = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    last_login_ip = db.Column(db.String(45), nullable=True)

    # 🔐 CAMPOS PARA CONTROL DE SESIÓN ÚNICA
    current_session_id = db.Column(db.String(100), nullable=True)
    session_ip = db.Column(db.String(45), nullable=True)
    session_user_agent = db.Column(db.String(500), nullable=True)
    last_activity = db.Column(db.DateTime, nullable=True)

    # Recuperación de contraseña
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relaciones
    role = db.relationship("Role", backref="primary_users", lazy=True)
    # Relación muchos-a-muchos: un usuario puede tener varios roles
    roles = db.relationship(
        "Role",
        secondary="user_roles",
        primaryjoin="User.id == UserRole.user_id",
        secondaryjoin="Role.id == UserRole.role_id",
        backref=db.backref("users", lazy="dynamic"),
        lazy="dynamic",
    )
    audit_logs = db.relationship(
        "AuditLog", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        """Establece la contraseña con hash seguro"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica la contraseña"""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        """Verifica si el usuario es administrador (por rol primario o asignado)"""
        if self.role and self.role.name == "admin":
            return True
        return self.has_role("admin")

    def is_locked(self):
        """Verifica si la cuenta está bloqueada"""
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False

    def lock_account(self, minutes=30):
        """Bloquea la cuenta por tiempo determinado"""
        self.locked_until = datetime.utcnow() + timedelta(minutes=minutes)
        self.failed_login_attempts = 0

    def unlock_account(self):
        """Desbloquea la cuenta"""
        self.locked_until = None
        self.failed_login_attempts = 0

    def increment_failed_login(self):
        """Incrementa intentos fallidos y bloquea si es necesario"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 3:
            self.lock_account()

    def reset_failed_login(self):
        """Resetea contador de intentos fallidos"""
        self.failed_login_attempts = 0
        self.locked_until = None

    def generate_2fa_secret(self):
        """Genera secreto para autenticación de dos factores"""
        if not self.two_factor_secret:
            self.two_factor_secret = pyotp.random_base32()
        return self.two_factor_secret

    def get_2fa_qr_code(self):
        """Genera código QR para configurar 2FA"""
        if not self.two_factor_secret:
            self.generate_2fa_secret()

        totp_uri = pyotp.totp.TOTP(self.two_factor_secret).provisioning_uri(
            name=self.email, issuer_name="MiloApps"
        )

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        return base64.b64encode(buffer.getvalue()).decode()

    def verify_2fa_token(self, token):
        """Verifica token de autenticación de dos factores"""
        if not self.two_factor_enabled or not self.two_factor_secret:
            return True

        totp = pyotp.TOTP(self.two_factor_secret)
        return totp.verify(token, valid_window=1)

    def generate_reset_token(self):
        """Genera token para recuperación de contraseña"""
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        return self.reset_token

    def verify_reset_token(self, token):
        """Verifica token de recuperación de contraseña"""
        if not self.reset_token or not self.reset_token_expires:
            return False

        if self.reset_token_expires < datetime.utcnow():
            return False

        return self.reset_token == token

    def clear_reset_token(self):
        """Limpia token de recuperación"""
        self.reset_token = None
        self.reset_token_expires = None

    @property
    def full_name(self):
        """Nombre completo del usuario"""
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        """Método para obtener nombre completo (compatibilidad con templates)"""
        return self.full_name

    def to_dict(self):
        """Convierte usuario a diccionario (sin datos sensibles)"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "company": self.company,
            "department": self.department,
            # mantener compatibilidad con clientes actuales
            "role": self.role.name if self.role else (self.get_primary_role_name()),
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "two_factor_enabled": self.two_factor_enabled,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "created_at": self.created_at.isoformat(),
        }

    # 🔐 MÉTODOS PARA CONTROL DE SESIÓN ÚNICA
    def start_session(self, session_id, ip_address, user_agent):
        """Inicia nueva sesión desplazando la anterior"""
        self.current_session_id = session_id
        self.session_ip = ip_address
        self.session_user_agent = user_agent
        self.last_activity = datetime.utcnow()
        self.last_login = datetime.utcnow()
        self.last_login_ip = ip_address

    def update_activity(self):
        """Actualiza timestamp de última actividad"""
        self.last_activity = datetime.utcnow()

    def clear_session(self):
        """Limpia datos de sesión actual"""
        self.current_session_id = None
        self.session_ip = None
        self.session_user_agent = None
        self.last_activity = None

    def has_active_session(self, session_id):
        """Verifica si el session_id coincide con el activo"""
        return self.current_session_id == session_id

    # ====== NUEVAS UTILIDADES DE ROLES Y PERMISOS ======
    def get_primary_role(self):
        """Devuelve el rol primario (compatibilidad). Si no hay role_id, retorna el primer rol asignado."""
        if self.role:
            return self.role
        return self.roles.first()

    def get_primary_role_name(self):
        r = self.get_primary_role()
        return r.name if r else None

    def has_role(self, role_name: str) -> bool:
        if (self.role and self.role.name == role_name) or (
            self.roles.filter_by(name=role_name).first()
        ):
            return True
        return False

    def has_allmilo(self) -> bool:
        """Retorna True si el usuario tiene el rol ALLMILO"""
        return self.has_role("ALLMILO")

    def has_app_access(self, app_key: str) -> bool:
        """Verifica acceso a una aplicación determinada.
        - Si tiene ALLMILO => True
        - Si algún rol tiene acceso total a esa app => True
        - Si tiene alguna funcionalidad en esa app => True
        """
        if self.has_allmilo():
            return True
        # roles asignados (incluye rol primario implícitamente vía relationship roles)
        user_roles = list(self.roles)
        if self.role and self.role not in user_roles:
            user_roles.append(self.role)

        for r in user_roles:
            if r.is_allmilo:
                return True
            # acceso total por app
            for ra in r.app_access:
                if ra.app and ra.app.key == app_key and ra.full_access:
                    return True
            # permisos granulares
            for rf in r.functionalities:
                if rf.functionality and rf.functionality.application and rf.functionality.application.key == app_key:
                    return True
        return False

    def has_functionality(self, app_key: str, functionality_key: str) -> bool:
        """Verifica permiso granular sobre una funcionalidad.
        - ALLMILO => True
        - full_access de rol sobre la app => True
        - rol con funcionalidad específica => True
        """
        if self.has_app_access(app_key):
            # has_app_access ya cubre ALLMILO y full_access
            # pero debemos validar granular solo si no hubo full_access
            if self.has_allmilo():
                return True
        # roles del usuario
        user_roles = list(self.roles)
        if self.role and self.role not in user_roles:
            user_roles.append(self.role)
        for r in user_roles:
            if r.is_allmilo:
                return True
            # full access?
            for ra in r.app_access:
                if ra.app and ra.app.key == app_key and ra.full_access:
                    return True
            # granular
            for rf in r.functionalities:
                if (
                    rf.functionality
                    and rf.functionality.key == functionality_key
                    and rf.functionality.application
                    and rf.functionality.application.key == app_key
                ):
                    return True
        return False


class Role(db.Model):
    """Modelo de Roles del Sistema con soporte para Apps y Funcionalidades"""

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    # Campo legacy de permisos en JSON (se mantiene por compatibilidad)
    permissions = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    # Nuevo: acceso global a todas las apps
    is_allmilo = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relaciones hacia aplicaciones/funcionalidades
    app_access = db.relationship(
        "RoleAppAccess", backref="role", lazy=True, cascade="all, delete-orphan"
    )
    functionalities = db.relationship(
        "RoleFunctionality", backref="role", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Role {self.name}>"

    # Métodos legacy
    def get_permissions(self):
        if self.permissions:
            return json.loads(self.permissions)
        return []

    def set_permissions(self, permissions_list):
        self.permissions = json.dumps(permissions_list)

    def has_permission(self, permission):
        permissions = self.get_permissions()
        return permission in permissions


# ====== NUEVAS TABLAS PARA APLICACIONES Y FUNCIONALIDADES ======
class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False, index=True)  # ej: milosign
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    functionalities = db.relationship(
        "Functionality", backref="application", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Application {self.key}>"


class Functionality(db.Model):
    __tablename__ = "functionalities"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"), nullable=False)
    key = db.Column(db.String(100), nullable=False, index=True)  # ej: create_document
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    __table_args__ = (db.UniqueConstraint("application_id", "key", name="uq_func_app_key"),)

    def __repr__(self):
        return f"<Functionality {self.key} of app {self.application_id}>"


# ====== TABLAS DE ASOCIACIÓN ======
class UserRole(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False, index=True)
    granted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    granted_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    __table_args__ = (db.UniqueConstraint("user_id", "role_id", name="uq_user_role"),)


class RoleAppAccess(db.Model):
    __tablename__ = "role_app_access"
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False, index=True)
    app_id = db.Column(db.Integer, db.ForeignKey("applications.id"), nullable=False, index=True)
    full_access = db.Column(db.Boolean, default=False, nullable=False)
    __table_args__ = (db.UniqueConstraint("role_id", "app_id", name="uq_role_app"),)

    app = db.relationship("Application", backref=db.backref("role_access", lazy=True))


class RoleFunctionality(db.Model):
    __tablename__ = "role_functionalities"
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False, index=True)
    functionality_id = db.Column(
        db.Integer, db.ForeignKey("functionalities.id"), nullable=False, index=True
    )
    __table_args__ = (
        db.UniqueConstraint("role_id", "functionality_id", name="uq_role_functionality"),
    )

    functionality = db.relationship(
        "Functionality", backref=db.backref("role_permissions", lazy=True)
    )


class AuditLog(db.Model):
    """Modelo de Log de Auditoría"""

    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    # Información del evento
    event_type = db.Column(db.String(50), nullable=False, index=True)
    event_description = db.Column(db.Text, nullable=True)
    resource_type = db.Column(db.String(50), nullable=True)
    resource_id = db.Column(db.String(100), nullable=True)

    # Información de la sesión
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    browser = db.Column(db.String(100), nullable=True)
    operating_system = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(200), nullable=True)

    # Datos adicionales
    additional_data = db.Column(db.Text, nullable=True)  # JSON string
    success = db.Column(db.Boolean, default=True, nullable=False)

    # Timestamp
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, index=True
    )

    def __repr__(self):
        return f"<AuditLog {self.event_type} by User {self.user_id}>"

    def set_additional_data(self, data_dict):
        """Establece datos adicionales como JSON"""
        # Asegurar serialización de datetime y otros tipos no JSON por defecto
        self.additional_data = json.dumps(
            data_dict,
            default=(
                lambda o: o.isoformat() if hasattr(o, "isoformat") else str(o)
            ),
        )

    def get_additional_data(self):
        """Obtiene datos adicionales como diccionario"""
        if self.additional_data:
            return json.loads(self.additional_data)
        return {}

    def to_dict(self):
        """Convierte log a diccionario"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_email": self.user.email if self.user else None,
            "event_type": self.event_type,
            "event_description": self.event_description,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "ip_address": self.ip_address,
            "browser": self.browser,
            "operating_system": self.operating_system,
            "location": self.location,
            "success": self.success,
            "created_at": self.created_at.isoformat(),
            "additional_data": self.get_additional_data(),
        }


def init_db(app):
    """Inicializa la base de datos con datos por defecto"""
    db.init_app(app)

    with app.app_context():
        # Crear todas las tablas
        db.create_all()

        # Migración ligera para SQLite: agregar columna is_allmilo si no existe
        try:
            conn = db.session.connection()
            res = conn.execute(db.text("PRAGMA table_info(roles)")).fetchall()
            cols = {row[1] for row in res} if res else set()
            if "is_allmilo" not in cols:
                conn.execute(
                    db.text(
                        "ALTER TABLE roles ADD COLUMN is_allmilo "
                        "BOOLEAN NOT NULL DEFAULT 0"
                    )
                )
                db.session.commit()
                print("✅ Migración aplicada: roles.is_allmilo agregado")
        except Exception:
            # Continuar sin bloquear si no aplica (otros motores o permisos)
            db.session.rollback()

        # Crear roles por defecto si no existen
        if not Role.query.first():
            admin_role = Role(
                name="admin",
                display_name="Administrador",
                description="Acceso completo al sistema y administración",
                permissions=json.dumps(
                    [
                        "user_management",
                        "system_config",
                        "audit_logs",
                        "all_reports",
                        "backup_restore",
                    ]
                ),
                is_allmilo=False,
            )

            user_role = Role(
                name="user",
                display_name="Usuario",
                description="Acceso básico al sistema",
                permissions=json.dumps(
                    ["profile_edit", "basic_reports", "data_entry"]
                ),
                is_allmilo=False,
            )

            allmilo_role = Role(
                name="ALLMILO",
                display_name="Acceso Global MiloApps",
                description=(
                    "Acceso total a todas las aplicaciones sin restricción"
                ),
                is_allmilo=True,
            )

            db.session.add_all([admin_role, user_role, allmilo_role])
            db.session.commit()

            print("✅ Roles por defecto creados: admin, user, ALLMILO")

        # Semillas de aplicaciones y funcionalidades básicas
        default_apps = [
            {
                "key": "milosign",
                "name": "MiloSign",
                "description": "Firma digital",
            },
            {
                "key": "contratacion",
                "name": "Contratación",
                "description": "Gestión de contratos",
            },
            {
                "key": "presupuesto",
                "name": "Presupuesto",
                "description": "Gestión de presupuestos",
            },
        ]

        for app_data in default_apps:
            app_row = Application.query.filter_by(key=app_data["key"]).first()
            if not app_row:
                app_row = Application(**app_data)
                db.session.add(app_row)
                db.session.flush()  # obtener id para funcionalidades

                # Funcionalidades ejemplo (granulares)
                default_funcs = [
                    {"key": "view", "name": "Ver"},
                    {"key": "create", "name": "Crear"},
                    {"key": "edit", "name": "Editar"},
                    {"key": "delete", "name": "Eliminar"},
                ]
                for f in default_funcs:
                    db.session.add(
                        Functionality(
                            application_id=app_row.id,
                            key=f["key"],
                            name=f["name"],
                        )
                    )

        db.session.commit()

        # Crear usuario administrador por defecto si no existe
        if not User.query.filter_by(email="admin@miloapps.com").first():
            admin_role = Role.query.filter_by(name="admin").first()
            allmilo_role = Role.query.filter_by(name="ALLMILO").first()

            admin_user = User(
                email="admin@miloapps.com",
                username="admin",
                first_name="Admin",
                last_name="MiloApps",
                role_id=admin_role.id if admin_role else None,
                is_active=True,
                is_verified=True,
            )
            admin_user.set_password("admin123")  # Cambiar en producción

            db.session.add(admin_user)
            db.session.flush()

            # Asignar roles admin y ALLMILO
            if admin_role:
                db.session.add(
                    UserRole(user_id=admin_user.id, role_id=admin_role.id)
                )
            if allmilo_role:
                db.session.add(
                    UserRole(user_id=admin_user.id, role_id=allmilo_role.id)
                )

            db.session.commit()

            print(
                "✅ Usuario administrador creado y roles asignados: "
                "admin, ALLMILO"
            )

        print("✅ Base de datos inicializada correctamente")


# Funciones de utilidad para auditoría
class AuditEvents:
    """Constantes para eventos de auditoría"""

    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILED = "login_failed"
    LOGOUT = "logout"
    PASSWORD_CHANGE = "password_change"
    PASSWORD_RESET_REQUEST = "password_reset_request"
    PASSWORD_RESET_SUCCESS = "password_reset_success"
    PROFILE_UPDATE = "profile_update"
    TWO_FACTOR_ENABLED = "two_factor_enabled"
    TWO_FACTOR_DISABLED = "two_factor_disabled"
    ACCOUNT_LOCKED = "account_locked"
    ACCOUNT_UNLOCKED = "account_unlocked"
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"
    PERMISSION_DENIED = "permission_denied"


def log_audit_event(
    user_id,
    event_type,
    description=None,
    resource_type=None,
    resource_id=None,
    request=None,
    success=True,
    additional_data=None,
):
    """Función para registrar eventos de auditoría"""
    try:
        audit_log = AuditLog(
            user_id=user_id,
            event_type=event_type,
            event_description=description,
            resource_type=resource_type,
            resource_id=resource_id,
            success=success,
        )

        if request:
            audit_log.ip_address = request.remote_addr
            audit_log.user_agent = str(request.user_agent)

            # Parsear user agent para obtener browser y OS
            from user_agents import parse

            ua = parse(request.user_agent.string)
            audit_log.browser = (
                f"{ua.browser.family} {ua.browser.version_string}"
            )
            audit_log.operating_system = (
                f"{ua.os.family} {ua.os.version_string}"
            )

        if additional_data:
            audit_log.set_additional_data(additional_data)

        db.session.add(audit_log)
        db.session.commit()

    except Exception as e:
        print(f"Error logging audit event: {e}")
        db.session.rollback()


def cleanup_old_audit_logs(months=6):
    """Limpia logs de auditoría antiguos (por defecto 6 meses)"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=months * 30)
        old_logs = (
            AuditLog.query.filter(AuditLog.created_at < cutoff_date).all()
        )

        count = len(old_logs)
        for log in old_logs:
            db.session.delete(log)

        db.session.commit()
        print(f"✅ Eliminados {count} logs de auditoría antiguos")
        return count

    except Exception as e:
        print(f"Error cleaning up audit logs: {e}")
        db.session.rollback()
        return 0
