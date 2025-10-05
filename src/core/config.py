# Core MiloApps - Configuración central
import os
from datetime import timedelta

class Config:
    """Configuración base para todas las aplicaciones de MiloApps"""
    
    # Configuración básica de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'miloapps-secret-key-2024'
    
    # Base de datos central
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///data/miloapps.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de email (compartida)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Configuración de sesiones
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuración de seguridad
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hora
    
    # Configuración de archivos
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    
    # Configuración de aplicaciones
    MILOAPPS_CONFIG = {
        'main_domain': os.environ.get('MAIN_DOMAIN', 'localhost:3000'),
        'enable_subdomains': os.environ.get('ENABLE_SUBDOMAINS', 'False').lower() == 'true',
        'default_app': 'auth',
        'company_name': 'MiloApps',
        'company_logo': '/static/img/logo.png',
        'support_email': 'support@miloapps.com'
    }
    
    # Configuración por aplicación
    APPS_CONFIG = {
        'auth': {
            'name': 'Autenticación',
            'description': 'Sistema de autenticación y gestión de usuarios',
            'icon': 'fa-shield-alt',
            'color': '#28a745',
            'requires_auth': False  # Esta app maneja la autenticación
        },
        'milosign': {
            'name': 'MiloSign',
            'description': 'Firma digital de documentos',
            'icon': 'fa-signature',
            'color': '#007bff',
            'requires_auth': True,
            'subdomain': 'milosign'
        },
        'contratacion': {
            'name': 'Contratación',
            'description': 'Gestión de contratos y contratación',
            'icon': 'fa-file-contract',
            'color': '#ffc107',
            'requires_auth': True,
            'subdomain': 'contratacion'
        },
        'presupuesto': {
            'name': 'Presupuesto',
            'description': 'Gestión de presupuestos y finanzas',
            'icon': 'fa-calculator',
            'color': '#17a2b8',
            'requires_auth': True,
            'subdomain': 'presupuesto'
        }
    }

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    DEVELOPMENT = True
    
class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    DEVELOPMENT = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Seleccionar configuración basada en el entorno
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(env_name='default'):
    """Obtener configuración por nombre de entorno"""
    return config_by_name.get(env_name, DevelopmentConfig)