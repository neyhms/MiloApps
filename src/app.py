# MiloApps Flask Application
# Aplicación web flexible para trabajo remoto con autenticación completa

import json
import os
import secrets
from datetime import datetime

from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

# Importar módulos de autenticación
from models import db, User, init_db, cleanup_old_audit_logs
from auth_routes import auth
from email_service import init_mail

# Cargar variables de entorno
load_dotenv()


class MiloAppsApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_config()
        self.setup_csrf()
        self.setup_database()
        self.setup_auth()
        self.setup_email()
        self.setup_cors()
        self.setup_moment()
        self.config = self.load_config()
        self.setup_routes()
        self.setup_error_handlers()

    def setup_config(self):
        """Configurar aplicación Flask"""
        # Configuración básica
        self.app.config["SECRET_KEY"] = os.environ.get(
            "SECRET_KEY"
        ) or secrets.token_hex(32)
        self.app.config["WTF_CSRF_ENABLED"] = True
        self.app.config["WTF_CSRF_TIME_LIMIT"] = 3600  # 1 hora

        # Base de datos SQLite
        db_path = os.path.join(os.path.dirname(__file__), "..", "data", "miloapps.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        # Configuración de seguridad
        self.app.config["SESSION_COOKIE_SECURE"] = False  # True en HTTPS
        self.app.config["SESSION_COOKIE_HTTPONLY"] = True
        self.app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

        # 🔐 CONFIGURACIÓN DE AUTO-LOGOUT Y SESIÓN ÚNICA
        from datetime import timedelta

        self.app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(
            minutes=30
        )  # 30 minutos
        self.app.config["SESSION_AUTO_LOGOUT"] = True
        self.app.config["SESSION_WARNING_TIME"] = 5  # Aviso 5 min antes
        self.app.config["SINGLE_SESSION_ENABLED"] = True  # Una sola sesión activa

        # Configuración de registro
        self.app.config["REGISTRATION_ENABLED"] = True

        print("✅ Configuración Flask establecida")

    def setup_csrf(self):
        """Habilitar CSRF global para formularios y endpoints POST."""
        CSRFProtect(self.app)
        # Excepciones específicas (si en el futuro hay endpoints API JSON)
    # from flask_wtf.csrf import CSRFError
        # @self.app.errorhandler(CSRFError)
        # def handle_csrf_error(e):
        #     return render_template('error.html', message=e.description), 400
        
    print("✅ CSRF Protection habilitado")

    def setup_database(self):
        """Configurar base de datos"""
        init_db(self.app)
        print("✅ Base de datos configurada")

    def setup_auth(self):
        """Configurar autenticación"""
        login_manager = LoginManager()
        login_manager.init_app(self.app)
        login_manager.login_view = "auth.login"
        login_manager.login_message = "Debes iniciar sesión para acceder a esta página."
        login_manager.login_message_category = "info"
        login_manager.refresh_view = "auth.login"
        login_manager.needs_refresh_message = (
            "Para proteger tu cuenta, confirma tu contraseña."
        )

        @login_manager.user_loader
        def load_user(user_id):
            try:
                return db.session.get(User, int(user_id))
            except Exception:
                return None

        # Registrar blueprint de autenticación
        self.app.register_blueprint(auth)

        # 🔐 MIDDLEWARE PARA CONTROL DE SESIÓN ÚNICA
        self.setup_session_middleware()

        print("✅ Sistema de autenticación configurado")

    def setup_session_middleware(self):
        """Configurar middleware para control de sesión única"""
        from flask import session, redirect, url_for, flash
        from flask_login import current_user, logout_user

        @self.app.before_request
        def validate_session():
            # Solo validar en rutas que requieren autenticación
            if current_user.is_authenticated:
                current_session_id = session.get("session_id")

                # Verificar si la sesión actual es válida
                if not current_user.has_active_session(current_session_id):
                    logout_user()
                    session.clear()
                    flash(
                        "Tu sesión ha sido desplazada por otro inicio de sesión.",
                        "warning",
                    )
                    return redirect(url_for("auth.login"))

                # Actualizar actividad del usuario
                current_user.update_activity()
                db.session.commit()

        print("✅ Middleware de sesión única configurado")

    def setup_email(self):
        """Configurar servicio de email"""
        init_mail(self.app)
        print("✅ Servicio de email configurado")

    def setup_cors(self):
        """Configurar CORS"""
        CORS(self.app, supports_credentials=True)
        print("✅ CORS configurado")

    def setup_moment(self):
        """Configurar Flask-Moment para fechas"""
        self.moment = Moment(self.app)

        # Agregar filtros personalizados para fechas
        @self.app.template_filter("datetime")
        def datetime_filter(date, format="%d/%m/%Y %H:%M"):
            if date:
                return date.strftime(format)
            return "N/A"

        @self.app.template_filter("timeago")
        def timeago_filter(date):
            if not date:
                return "Nunca"
            from datetime import datetime

            now = datetime.now()
            diff = now - date

            if diff.days > 0:
                return f"hace {diff.days} días"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"hace {hours} horas"
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"hace {minutes} minutos"
            else:
                return "hace unos segundos"

        print("✅ Flask-Moment configurado")

    def load_config(self):
        """Cargar configuración activa"""
        try:
            # Intentar cargar configuración activa
            config_path = os.path.join(
                os.path.dirname(__file__), "..", "config", "active.json"
            )
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                print(f"📋 Configuración cargada: {config['environment'].upper()}")
                return config
        except Exception as e:
            print(f"⚠️  Error cargando configuración activa: {e}")

        # Cargar configuración por defecto
        try:
            default_path = os.path.join(
                os.path.dirname(__file__), "..", "config", "default.json"
            )
            with open(default_path, "r", encoding="utf-8") as f:
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
            "development": {"port": 5000, "host": "127.0.0.1", "debug_mode": True},
        }

    def setup_routes(self):
        """Configurar rutas de la aplicación"""

        @self.app.route("/")
        def index():
            """Página principal"""
            if current_user.is_authenticated:
                return redirect(url_for("dashboard"))
            return render_template("index.html", config=self.config)

        @self.app.route("/dashboard")
        @login_required
        def dashboard():
            """Dashboard principal del usuario"""
            # Limpiar logs antiguos periódicamente
            cleanup_old_audit_logs()
            return render_template(
                "dashboard.html", config=self.config, user=current_user
            )

        @self.app.route("/api/config")
        @login_required
        def get_config():
            """API para obtener configuración"""
            return jsonify(self.config)

        @self.app.route("/api/status")
        def get_status():
            """API para obtener estado del sistema"""
            status_data = {
                "status": "running",
                "environment": self.config["environment"],
                "server": "Flask/Python",
                "port": self.config["development"]["port"],
                "host": self.config["development"]["host"],
                "debug": self.config["development"]["debug_mode"],
                "timestamp": datetime.now().isoformat(),
                "uptime": "Flask app running",
            }

            # Agregar información de usuario si está autenticado
            if current_user.is_authenticated:
                status_data["user"] = {
                    "id": current_user.id,
                    "username": current_user.username,
                    "email": current_user.email,
                    "role": current_user.role.name if current_user.role else "user",
                    "last_login": (
                        current_user.last_login.isoformat()
                        if current_user.last_login
                        else None
                    ),
                }

            return jsonify(status_data)
        
            @self.app.route("/api/activity")
            @login_required
            def get_user_activity():
                """API para obtener actividad reciente del usuario"""
                # MOCK DATA PARA PRUEBA DE FRONTEND
                print("⚡ Enviando datos de prueba de actividad reciente (mock)")
                activities = [
                    {
                        "id": 1,
                        "event_type": "login",
                        "event_description": "Inicio de sesión exitoso",
                        "success": True,
                        "ip_address": "192.168.1.10",
                        "browser": "Chrome",
                        "created_at": "2025-10-05T10:00:00",
                        "relative_time": "2025-10-05T10:00:00"
                    },
                    {
                        "id": 2,
                        "event_type": "profile_update",
                        "event_description": "Actualización de perfil",
                        "success": True,
                        "ip_address": "192.168.1.10",
                        "browser": "Firefox",
                        "created_at": "2025-10-04T18:30:00",
                        "relative_time": "2025-10-04T18:30:00"
                    },
                    {
                        "id": 3,
                        "event_type": "password_change",
                        "event_description": "Cambio de contraseña",
                        "success": True,
                        "ip_address": "192.168.1.10",
                        "browser": "Edge",
                        "created_at": "2025-10-03T09:15:00",
                        "relative_time": "2025-10-03T09:15:00"
                    }
                ]
                return jsonify({
                    "activities": activities,
                    "total": len(activities),
                    "user_id": current_user.id,
                    "mock": True
                })

        @self.app.route("/api/switch-env", methods=["POST"])
        @login_required
        def switch_environment():
            """API para cambiar configuración (solo administradores)"""
            if not current_user.role or current_user.role.name != "admin":
                return jsonify({"error": "Acceso denegado"}), 403

            data = request.get_json()
            env = data.get("environment", "default")

            try:
                # Cargar nueva configuración
                config_path = os.path.join(
                    os.path.dirname(__file__), "..", "config", f"{env}.json"
                )
                if not os.path.exists(config_path):
                    return jsonify({"error": f"Configuración {env} no encontrada"}), 404

                with open(config_path, "r", encoding="utf-8") as f:
                    new_config = json.load(f)

                # Guardar como configuración activa
                active_path = os.path.join(
                    os.path.dirname(__file__), "..", "config", "active.json"
                )
                with open(active_path, "w", encoding="utf-8") as f:
                    json.dump(new_config, f, indent=2, ensure_ascii=False)

                # Actualizar configuración en memoria
                self.config = new_config

                return jsonify(
                    {
                        "success": True,
                        "environment": env,
                        "message": f"Configuración cambiada a {env.upper()}",
                        "config": new_config,
                    }
                )

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route("/docs")
        def docs():
            """Página de documentación"""
            return render_template("docs.html")

    def setup_error_handlers(self):
        """Configurar manejadores de error"""

        @self.app.errorhandler(400)
        def bad_request(error):
            return (
                render_template(
                    "error.html", error_code=400, error_message="Solicitud incorrecta"
                ),
                400,
            )

        @self.app.errorhandler(403)
        def forbidden(error):
            return (
                render_template(
                    "error.html", error_code=403, error_message="Acceso denegado"
                ),
                403,
            )

        @self.app.errorhandler(404)
        def not_found(error):
            return render_template("404.html"), 404

        @self.app.errorhandler(429)
        def rate_limit_exceeded(error):
            return (
                render_template(
                    "error.html",
                    error_code=429,
                    error_message="Demasiadas solicitudes. Intenta más tarde.",
                ),
                429,
            )

        @self.app.errorhandler(500)
        def internal_error(error):
            return (
                render_template(
                    "error.html",
                    error_code=500,
                    error_message="Error interno del servidor",
                ),
                500,
            )

    def run(self):
        """Iniciar la aplicación"""
        host = self.config["development"]["host"]
        port = self.config["development"]["port"]
        debug = self.config["development"]["debug_mode"]

        print("🚀 Iniciando MiloApps Flask App...")
        print(f'📍 Entorno: {self.config["environment"]}')
        print(f"🌐 URL: http://{host}:{port}")
        print(f'🐛 Debug: {"ACTIVADO" if debug else "DESACTIVADO"}')

        if self.config.get("network", {}).get("proxy"):
            print("🔗 Proxy: Configurado")

        print("")
        print("Endpoints disponibles:")
        print(f"   📄 Home: http://{host}:{port}/")
        print(f"   ⚙️  Config: http://{host}:{port}/api/config")
        print(f"   📊 Status: http://{host}:{port}/api/status")
        print(f"   📖 Docs: http://{host}:{port}/docs")
        print("")

        self.app.run(host=host, port=port, debug=debug)


# Crear y ejecutar la aplicación
if __name__ == "__main__":
    app = MiloAppsApp()
    app.run()
