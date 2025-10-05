#!/usr/bin/env python3
# Test script para verificar dependencias

print("🔍 Verificando dependencias de InfoMilo...")

try:
    from flask import Flask
    print("✅ Flask importado correctamente")
except ImportError as e:
    print(f"❌ Error importando Flask: {e}")

try:
    from flask_sqlalchemy import SQLAlchemy
    print("✅ Flask-SQLAlchemy importado correctamente")
except ImportError as e:
    print(f"❌ Error importando Flask-SQLAlchemy: {e}")

try:
    from flask_login import LoginManager
    print("✅ Flask-Login importado correctamente")
except ImportError as e:
    print(f"❌ Error importando Flask-Login: {e}")

try:
    from flask_wtf import FlaskForm
    print("✅ Flask-WTF importado correctamente")
except ImportError as e:
    print(f"❌ Error importando Flask-WTF: {e}")

try:
    from flask_mail import Mail
    print("✅ Flask-Mail importado correctamente")
except ImportError as e:
    print(f"❌ Error importando Flask-Mail: {e}")

try:
    import bcrypt
    print("✅ bcrypt importado correctamente")
except ImportError as e:
    print(f"❌ Error importando bcrypt: {e}")

print("\n🔍 Probando importaciones locales...")

try:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    
    from models import User, Role
    print("✅ Modelos importados correctamente")
except ImportError as e:
    print(f"❌ Error importando modelos: {e}")

print("\n✅ Verificación completa!")
