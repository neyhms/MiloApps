# InfoMilo Flask Application
# Aplicación web flexible para trabajo remoto

import json
import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class InfoMiloApp:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.config = self.load_config()
        self.setup_routes()
        
    def load_config(self):
        """Cargar configuración activa"""
        try:
            # Intentar cargar configuración activa
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'active.json')
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                print(f"📋 Configuración cargada: {config['environment'].upper()}")
                return config
        except Exception as e:
            print(f"⚠️  Error cargando configuración activa: {e}")
        
        # Cargar configuración por defecto
        try:
            default_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'default.json')
            with open(default_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print("📋 Usando configuración por defecto")
            return config
        except Exception as e:
            print(f"❌ Error cargando configuración: {e}")
            return self.get_fallback_config()
    
    def get_fallback_config(self):
        """Configuración de respaldo si no se pueden cargar los archivos"""
        return {
            "environment": "fallback",
            "description": "Configuración de respaldo",
            "development": {
                "port": 5000,
                "host": "127.0.0.1",
                "debug_mode": True
            }
        }
    
    def setup_routes(self):
        """Configurar rutas de la aplicación"""
        
        @self.app.route('/')
        def index():
            """Página principal"""
            return render_template('index.html', config=self.config)
        
        @self.app.route('/api/config')
        def get_config():
            """API para obtener configuración"""
            return jsonify(self.config)
        
        @self.app.route('/api/status')
        def get_status():
            """API para obtener estado del sistema"""
            return jsonify({
                'status': 'running',
                'environment': self.config['environment'],
                'server': 'Flask/Python',
                'port': self.config['development']['port'],
                'host': self.config['development']['host'],
                'debug': self.config['development']['debug_mode'],
                'timestamp': datetime.now().isoformat(),
                'uptime': 'Flask app running'
            })
        
        @self.app.route('/api/switch-env', methods=['POST'])
        def switch_environment():
            """API para cambiar configuración"""
            data = request.get_json()
            env = data.get('environment', 'default')
            
            try:
                # Cargar nueva configuración
                config_path = os.path.join(os.path.dirname(__file__), '..', 'config', f'{env}.json')
                if not os.path.exists(config_path):
                    return jsonify({'error': f'Configuración {env} no encontrada'}), 404
                
                with open(config_path, 'r', encoding='utf-8') as f:
                    new_config = json.load(f)
                
                # Guardar como configuración activa
                active_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'active.json')
                with open(active_path, 'w', encoding='utf-8') as f:
                    json.dump(new_config, f, indent=2, ensure_ascii=False)
                
                # Actualizar configuración en memoria
                self.config = new_config
                
                return jsonify({
                    'success': True,
                    'environment': env,
                    'message': f'Configuración cambiada a {env.upper()}',
                    'config': new_config
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/docs')
        def docs():
            """Página de documentación"""
            return render_template('docs.html')
        
        @self.app.errorhandler(404)
        def not_found(error):
            return render_template('404.html'), 404
    
    def run(self):
        """Iniciar la aplicación"""
        host = self.config['development']['host']
        port = self.config['development']['port']
        debug = self.config['development']['debug_mode']
        
        print('🚀 Iniciando InfoMilo Flask App...')
        print(f'📍 Entorno: {self.config["environment"]}')
        print(f'🌐 URL: http://{host}:{port}')
        print(f'🐛 Debug: {"ACTIVADO" if debug else "DESACTIVADO"}')
        
        if self.config.get('network', {}).get('proxy'):
            print('🔗 Proxy: Configurado')
        
        print('')
        print('Endpoints disponibles:')
        print(f'   📄 Home: http://{host}:{port}/')
        print(f'   ⚙️  Config: http://{host}:{port}/api/config')
        print(f'   📊 Status: http://{host}:{port}/api/status')
        print(f'   📖 Docs: http://{host}:{port}/docs')
        print('')
        
        self.app.run(host=host, port=port, debug=debug)

# Crear y ejecutar la aplicación
if __name__ == '__main__':
    app = InfoMiloApp()
    app.run()
