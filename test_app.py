# MiloApps - Version de prueba de la nueva estructura modular
import os
import sys
import json
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def create_test_app():
    """Crear aplicación de prueba con la nueva estructura"""
    
    app = Flask(__name__, 
                template_folder='src/templates',
                static_folder='src/static')
    
    app.config['SECRET_KEY'] = 'test-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/miloapps.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configurar Flask-Login básico
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return None  # Placeholder por ahora
    
    # Ruta principal
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')
    
    @app.route('/test-structure')
    def test_structure():
        """Endpoint para probar que la estructura funciona"""
        structure_info = {
            'core_available': os.path.exists('src/core'),
            'auth_app_available': os.path.exists('src/apps/auth'),
            'milosign_app_available': os.path.exists('src/apps/milosign'),
            'templates_available': os.path.exists('src/templates'),
            'config_loaded': os.path.exists('config/active.json')
        }
        
        return {
            'status': 'success',
            'message': 'Nueva estructura modular funcionando',
            'structure': structure_info,
            'apps_available': [
                {'name': 'auth', 'display': 'Autenticación', 'url': '/auth'},
                {'name': 'milosign', 'display': 'MiloSign', 'url': '/milosign'},
                {'name': 'contratacion', 'display': 'Contratación', 'url': '/contratacion'},
                {'name': 'presupuesto', 'display': 'Presupuesto', 'url': '/presupuesto'}
            ]
        }
    
    return app

if __name__ == '__main__':
    print("🚀 INICIANDO MILOAPPS - ESTRUCTURA MODULAR DE PRUEBA")
    print("=" * 60)
    
    app = create_test_app()
    
    # Cargar configuración si existe
    config_file = 'config/active.json'
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            env_config = json.load(f)
        
        port = env_config.get('development', {}).get('port', 3000)
        print(f"🏠 Configuración: {env_config.get('environment', 'development').upper()}")
        print(f"🌐 URL: http://localhost:{port}")
        print(f"🧪 Test: http://localhost:{port}/test-structure")
        print("")
        print("📋 ESTRUCTURA MODULAR:")
        print("   📦 Core: Sistema compartido (models, utils, config)")
        print("   🔐 Auth: Sistema de autenticación")
        print("   ✍️ MiloSign: Firma digital")
        print("   📋 Contratación: Gestión de contratos") 
        print("   💰 Presupuesto: Gestión financiera")
        print("")
        
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        print("⚠️ Usando configuración por defecto")
        app.run(host='0.0.0.0', port=3000, debug=True)