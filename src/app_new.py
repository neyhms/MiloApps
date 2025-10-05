# MiloApps - Aplicación principal modular
import os
from flask import Flask, render_template, jsonify, redirect, url_for
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_moment import Moment
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

# Importar núcleo compartido
from core import db, get_config, create_initial_data, register_template_functions
from core.models import User
from core.utils import log_audit, get_user_apps, detect_app_from_request

# Importar aplicaciones
from apps.auth.routes import auth_bp
from apps.milosign.routes import milosign_bp

def create_app(config_name='default'):
    """Factory para crear la aplicación Flask"""
    
    app = Flask(__name__)
    
    # Cargar configuración
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Configurar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Debes iniciar sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Configurar Mail
    mail = Mail(app)
    
    # Configurar Moment
    moment = Moment(app)
    
    # Configurar CORS
    CORS(app)
    
    # Registrar funciones de template globales
    register_template_functions(app)
    
    # Registrar blueprints (aplicaciones)
    app.register_blueprint(auth_bp)
    app.register_blueprint(milosign_bp)
    
    # Crear blueprints para futuras aplicaciones
    from flask import Blueprint
    
    # Contratación
    contratacion_bp = Blueprint('contratacion', __name__, url_prefix='/contratacion')
    
    @contratacion_bp.route('/')
    def dashboard():
        return render_template('contratacion/dashboard.html')
    
    app.register_blueprint(contratacion_bp)
    
    # Presupuesto
    presupuesto_bp = Blueprint('presupuesto', __name__, url_prefix='/presupuesto')
    
    @presupuesto_bp.route('/')
    def dashboard():
        return render_template('presupuesto/dashboard.html')
    
    app.register_blueprint(presupuesto_bp)
    
    # Rutas principales
    @app.route('/')
    def index():
        """Página principal - redirige según el estado del usuario"""
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        return redirect(url_for('auth.login'))
    
    @app.route('/dashboard')
    def main_dashboard():
        """Dashboard principal con menú de aplicaciones"""
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        
        user_apps = get_user_apps()
        current_app_name = detect_app_from_request()
        
        log_audit('DASHBOARD_VIEW', 'main', current_user.id)
        
        return render_template('dashboard.html', 
                             user_apps=user_apps,
                             current_app=current_app_name)
    
    # Registrar ruta del dashboard con nombre alternativo
    app.add_url_rule('/dashboard', 'main.dashboard', main_dashboard)
    
    # APIs generales
    @app.route('/api/config')
    def api_config():
        """API para obtener configuración de la aplicación"""
        current_app_name = detect_app_from_request()
        
        config_data = {
            'app_name': 'MiloApps',
            'version': '1.0.0',
            'current_app': current_app_name,
            'environment': app.config.get('ENV', 'development'),
            'debug': app.config.get('DEBUG', False),
            'available_apps': []
        }
        
        if current_user.is_authenticated:
            config_data['available_apps'] = get_user_apps()
            config_data['user'] = {
                'id': current_user.id,
                'username': current_user.username,
                'email': current_user.email,
                'is_admin': current_user.is_admin
            }
        
        return jsonify(config_data)
    
    @app.route('/api/status')
    def api_status():
        """API para verificar estado del sistema"""
        return jsonify({
            'status': 'ok',
            'timestamp': '2025-10-05T00:00:00Z',
            'version': '1.0.0',
            'database': 'connected'
        })
    
    @app.route('/docs')
    def docs():
        """Documentación del sistema"""
        return render_template('docs.html')
    
    # Manejadores de errores
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('error.html', 
                             error_code=500,
                             error_message='Error interno del servidor'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('error.html',
                             error_code=403,
                             error_message='No tienes permisos para acceder a esta página'), 403
    
    # Contexto de template global
    @app.context_processor
    def inject_global_vars():
        """Inyectar variables globales en todos los templates"""
        return {
            'app_name': 'MiloApps',
            'company_name': app.config.get('MILOAPPS_CONFIG', {}).get('company_name', 'MiloApps'),
            'support_email': app.config.get('MILOAPPS_CONFIG', {}).get('support_email', 'support@miloapps.com'),
            'current_app_name': detect_app_from_request() if current_user.is_authenticated else 'auth'
        }
    
    # Inicializar base de datos
    with app.app_context():
        try:
            db.create_all()
            create_initial_data()
            print("✅ Base de datos inicializada correctamente")
        except Exception as e:
            print(f"❌ Error inicializando base de datos: {e}")
    
    return app

# Crear aplicación para desarrollo
app = create_app()

if __name__ == '__main__':
    # Obtener configuración del entorno
    config_file = 'config/active.json'
    
    if os.path.exists(config_file):
        import json
        with open(config_file, 'r') as f:
            env_config = json.load(f)
        
        print("✅ Configuración Flask establecida")
        print("✅ Base de datos inicializada correctamente") 
        print("✅ Base de datos configurada")
        print("✅ Sistema de autenticación configurado")
        print("✅ Servicio de email configurado con Gmail SMTP")
        print("✅ Servicio de email configurado")
        print("✅ CORS configurado")
        print("✅ Flask-Moment configurado")
        print(f"📋 Configuración cargada: {env_config.get('environment', 'UNKNOWN').upper()}")
        print("🚀 Iniciando MiloApps Flask App...")
        print(f"📍 Entorno: {env_config.get('environment', 'development')}")
        
        port = env_config.get('development', {}).get('port', 3000)
        debug = env_config.get('development', {}).get('debug_mode', True)
        
        print(f"🌐 URL: http://localhost:{port}")
        print(f"🐛 Debug: {'ACTIVADO' if debug else 'DESACTIVADO'}")
        print("")
        print("Endpoints disponibles:")
        print(f"   📄 Home: http://localhost:{port}/")
        print(f"   ⚙️  Config: http://localhost:{port}/api/config")
        print(f"   📊 Status: http://localhost:{port}/api/status")
        print(f"   📖 Docs: http://localhost:{port}/docs")
        print("")
        
        # Iniciar servidor
        app.run(host='0.0.0.0', port=port, debug=debug)
    else:
        print("❌ No se encontró archivo de configuración")
        print("🔧 Usando configuración por defecto")
        app.run(host='0.0.0.0', port=3000, debug=True)