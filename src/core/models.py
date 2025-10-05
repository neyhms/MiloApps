# Core MiloApps - Modelos compartidos entre aplicaciones
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pyotp
import qrcode
from io import BytesIO
import base64

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Modelo de Usuario compartido entre todas las aplicaciones de MiloApps"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    # Perfil
    first_name = db.Column(db.String(80), nullable=False, default='')
    last_name = db.Column(db.String(80), nullable=False, default='')
    bio = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    avatar = db.Column(db.String(200), nullable=True)
    
    # Estado y seguridad
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    email_verified = db.Column(db.Boolean, default=False)
    
    # 2FA
    two_factor_secret = db.Column(db.String(32), nullable=True)
    two_factor_enabled = db.Column(db.Boolean, default=False)
    backup_codes = db.Column(db.Text, nullable=True)
    
    # Control de acceso
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones con aplicaciones
    audit_logs = db.relationship('AuditLog', backref='user_ref', lazy=True)
    user_apps = db.relationship('UserAppPermission', backref='user_ref', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
        
    def generate_2fa_secret(self):
        """Generar secreto para 2FA"""
        self.two_factor_secret = pyotp.random_base32()
        return self.two_factor_secret
        
    def get_2fa_qr_code(self, app_name="MiloApps"):
        """Generar código QR para 2FA"""
        if not self.two_factor_secret:
            self.generate_2fa_secret()
            
        totp_uri = pyotp.totp.TOTP(self.two_factor_secret).provisioning_uri(
            name=self.email,
            issuer_name=app_name
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
        
    def verify_2fa_token(self, token):
        """Verificar token 2FA"""
        if not self.two_factor_secret:
            return False
            
        totp = pyotp.TOTP(self.two_factor_secret)
        return totp.verify(token, valid_window=1)
        
    def has_app_permission(self, app_name):
        """Verificar si el usuario tiene permisos para una aplicación específica"""
        return any(perm.app_name == app_name and perm.is_active 
                  for perm in self.user_apps)
        
    def get_app_role(self, app_name):
        """Obtener rol del usuario en una aplicación específica"""
        for perm in self.user_apps:
            if perm.app_name == app_name and perm.is_active:
                return perm.role
        return None
        
    def __repr__(self):
        return f'<User {self.username}>'


class UserAppPermission(db.Model):
    """Permisos de usuario por aplicación"""
    __tablename__ = 'user_app_permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    app_name = db.Column(db.String(50), nullable=False)  # 'milosign', 'contratacion', etc.
    role = db.Column(db.String(50), nullable=False, default='user')  # 'admin', 'user', 'readonly'
    is_active = db.Column(db.Boolean, default=True)
    granted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    granted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserAppPermission {self.user_id}:{self.app_name}:{self.role}>'


class AuditLog(db.Model):
    """Log de auditoría compartido entre aplicaciones"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    app_name = db.Column(db.String(50), nullable=False)  # Aplicación que genera el log
    action = db.Column(db.String(100), nullable=False)  # Acción realizada
    resource_type = db.Column(db.String(50), nullable=True)  # Tipo de recurso afectado
    resource_id = db.Column(db.String(50), nullable=True)  # ID del recurso afectado
    details = db.Column(db.Text, nullable=True)  # Detalles adicionales en JSON
    ip_address = db.Column(db.String(45), nullable=True)  # IPv4 o IPv6
    user_agent = db.Column(db.String(500), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<AuditLog {self.action} by {self.user_id} in {self.app_name}>'


class AppConfig(db.Model):
    """Configuración de aplicaciones"""
    __tablename__ = 'app_configs'
    
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(50), nullable=False, unique=True)
    display_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(50), nullable=True, default='fa-cog')
    color = db.Column(db.String(7), nullable=True, default='#007bff')
    is_active = db.Column(db.Boolean, default=True)
    requires_admin = db.Column(db.Boolean, default=False)
    url_prefix = db.Column(db.String(50), nullable=False)
    subdomain = db.Column(db.String(50), nullable=True)
    order_index = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<AppConfig {self.app_name}>'


# Función para crear datos iniciales
def create_initial_data():
    """Crear datos iniciales para el sistema"""
    
    # Crear usuario administrador si no existe
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@miloapps.com',
            first_name='Administrador',
            last_name='MiloApps',
            is_admin=True,
            email_verified=True
        )
        admin.set_password('MiloAdmin2024!')
        db.session.add(admin)
    
    # Crear configuración de aplicaciones
    apps_config = [
        {
            'app_name': 'auth',
            'display_name': 'Autenticación',
            'description': 'Sistema de autenticación y gestión de usuarios',
            'icon': 'fa-shield-alt',
            'color': '#28a745',
            'url_prefix': '/auth',
            'order_index': 1
        },
        {
            'app_name': 'milosign',
            'display_name': 'MiloSign',
            'description': 'Firma digital de documentos',
            'icon': 'fa-signature',
            'color': '#007bff',
            'url_prefix': '/milosign',
            'subdomain': 'milosign',
            'order_index': 2
        },
        {
            'app_name': 'contratacion',
            'display_name': 'Contratación',
            'description': 'Gestión de contratos y contratación',
            'icon': 'fa-file-contract',
            'color': '#ffc107',
            'url_prefix': '/contratacion',
            'subdomain': 'contratacion',
            'order_index': 3
        },
        {
            'app_name': 'presupuesto',
            'display_name': 'Presupuesto',
            'description': 'Gestión de presupuestos y finanzas',
            'icon': 'fa-calculator',
            'color': '#17a2b8',
            'url_prefix': '/presupuesto',
            'subdomain': 'presupuesto',
            'order_index': 4
        }
    ]
    
    for app_data in apps_config:
        existing_app = AppConfig.query.filter_by(app_name=app_data['app_name']).first()
        if not existing_app:
            app_config = AppConfig(**app_data)
            db.session.add(app_config)
    
    # Dar permisos al admin para todas las aplicaciones
    if admin:
        for app_data in apps_config:
            existing_perm = UserAppPermission.query.filter_by(
                user_id=admin.id, 
                app_name=app_data['app_name']
            ).first()
            if not existing_perm:
                perm = UserAppPermission(
                    user_id=admin.id,
                    app_name=app_data['app_name'],
                    role='admin'
                )
                db.session.add(perm)
    
    db.session.commit()