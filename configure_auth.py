#!/usr/bin/env python3
"""
InfoMilo - Configuración Rápida del Sistema de Autenticación
Script para configurar rápidamente el sistema después de la instalación
"""

import os
import secrets
import sqlite3
from pathlib import Path

def generate_secret_key():
    """Generar una clave secreta segura"""
    return secrets.token_hex(32)

def create_env_file():
    """Crear archivo .env con configuración básica"""
    env_path = Path('.env')
    
    if env_path.exists():
        print("⚠️  El archivo .env ya existe. Creando backup...")
        import shutil
        shutil.copy('.env', '.env.backup')
    
    secret_key = generate_secret_key()
    
    env_content = f"""# InfoMilo Environment Variables
# Generado automáticamente - Personaliza según tus necesidades

# Flask Configuration
SECRET_KEY={secret_key}
FLASK_ENV=development

# Database Configuration
DATABASE_URL=sqlite:///data/infomilo.db

# Email Configuration (Gmail SMTP)
# IMPORTANTE: Configura estos valores para que funcione el email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_app_password_de_gmail
MAIL_DEFAULT_SENDER=tu_email@gmail.com

# Security Configuration
PASSWORD_MIN_LENGTH=8
MAX_LOGIN_ATTEMPTS=3
SESSION_TIMEOUT=3600

# Application Configuration
APP_NAME=InfoMilo
APP_URL=http://localhost:3000
ADMIN_EMAIL=admin@infomilo.com

# Development/Debug
DEBUG=True
TESTING=False

# Rate Limiting
RATELIMIT_STORAGE_URL=memory://
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Archivo .env creado exitosamente")
    return True

def check_database():
    """Verificar que la base de datos se pueda crear"""
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    db_path = data_dir / 'infomilo.db'
    
    try:
        # Prueba de conexión
        conn = sqlite3.connect(str(db_path))
        conn.close()
        print(f"✅ Base de datos accesible en: {db_path}")
        return True
    except Exception as e:
        print(f"❌ Error con base de datos: {e}")
        return False

def check_dependencies():
    """Verificar que todas las dependencias estén instaladas"""
    required_packages = {
        'flask': 'Flask',
        'flask_sqlalchemy': 'Flask-SQLAlchemy',
        'flask_login': 'Flask-Login',
        'flask_wtf': 'Flask-WTF',
        'flask_mail': 'Flask-Mail',
        'bcrypt': 'bcrypt',
        'pyotp': 'pyotp',
        'qrcode': 'qrcode',
        'user_agents': 'user-agents',
        'wtforms': 'WTForms'
    }
    
    missing = []
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            missing.append(name)
            print(f"❌ {name} - FALTANTE")
    
    if missing:
        print(f"\n⚠️  Paquetes faltantes: {', '.join(missing)}")
        print("💡 Para instalarlos ejecuta:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    print("\n✅ Todas las dependencias están instaladas")
    return True

def setup_gmail_instructions():
    """Mostrar instrucciones para configurar Gmail"""
    print("\n" + "="*60)
    print("📧 CONFIGURACIÓN DE GMAIL SMTP")
    print("="*60)
    print("""
Para que funcione el envío de emails, necesitas configurar Gmail:

1. Ve a tu cuenta de Google: https://myaccount.google.com/
2. Seguridad > Verificación en 2 pasos (debe estar ACTIVADA)
3. Contraseñas de aplicaciones > Crear nueva contraseña de aplicación
4. Selecciona "Correo" y "Otro" (escribe "InfoMilo")
5. Copia la contraseña de 16 caracteres generada
6. Edita el archivo .env y reemplaza:
   - MAIL_USERNAME=tu_email@gmail.com
   - MAIL_PASSWORD=la_contraseña_de_16_caracteres

⚠️  IMPORTANTE: 
- NO uses tu contraseña normal de Gmail
- DEBES usar la "Contraseña de aplicación" generada
- La verificación en 2 pasos DEBE estar activada

✅ Una vez configurado, el sistema podrá enviar:
- Emails de recuperación de contraseña
- Emails de bienvenida
- Alertas de seguridad
""")

def show_next_steps():
    """Mostrar los siguientes pasos"""
    print("\n" + "="*60)
    print("🚀 PRÓXIMOS PASOS")
    print("="*60)
    print("""
1. Configurar Gmail SMTP (ver instrucciones arriba)

2. Iniciar la aplicación:
   python src/app.py

3. Abrir navegador en: http://localhost:3000

4. Login inicial:
   Usuario: admin@infomilo.com
   Contraseña: admin123

5. CAMBIAR la contraseña del administrador inmediatamente

6. Crear usuarios adicionales desde el panel de admin

7. Configurar 2FA para mayor seguridad

8. Para trabajo flexible casa/oficina:
   .\scripts\work-manager.ps1
""")

def main():
    """Función principal de configuración"""
    print("🔐 InfoMilo - Configuración del Sistema de Autenticación")
    print("="*60)
    
    # Verificar dependencias
    print("\n📦 Verificando dependencias...")
    if not check_dependencies():
        print("\n❌ Instala las dependencias faltantes antes de continuar")
        return
    
    # Crear archivo .env
    print("\n⚙️  Configurando variables de entorno...")
    if not create_env_file():
        print("\n❌ Error creando archivo .env")
        return
    
    # Verificar base de datos
    print("\n🗄️  Verificando base de datos...")
    if not check_database():
        print("\n❌ Error con la base de datos")
        return
    
    # Mostrar instrucciones de Gmail
    setup_gmail_instructions()
    
    # Mostrar próximos pasos
    show_next_steps()
    
    print("\n" + "="*60)
    print("✅ CONFIGURACIÓN COMPLETADA")
    print("="*60)
    print("El sistema de autenticación está listo para usar!")
    print("Recuerda configurar Gmail SMTP para el envío de emails.")

if __name__ == "__main__":
    main()
