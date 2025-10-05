#!/usr/bin/env python3
"""
Script para probar login directamente
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from models import db, User, init_db
from flask import Flask

def test_login(email, password):
    """Probar login con credenciales específicas"""
    
    # Configurar Flask app temporal
    app = Flask(__name__)
    
    # Configuración básica
    app.config['SECRET_KEY'] = 'temp-key-for-login-test'
    
    # Base de datos SQLite
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'infomilo.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar base de datos
    init_db(app)
    
    with app.app_context():
        print(f"🧪 Probando login con:")
        print(f"   Email: {email}")
        print(f"   Contraseña: {password}")
        print("-" * 50)
        
        # Buscar usuario
        user = User.query.filter_by(email=email).first()
        
        if not user:
            print(f"❌ Usuario con email '{email}' NO encontrado")
            print("📋 Emails disponibles:")
            all_users = User.query.all()
            for u in all_users:
                print(f"   - {u.email}")
            return False
        
        print(f"✅ Usuario encontrado:")
        print(f"   ID: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Username: {user.username}")
        print(f"   Nombre: {user.first_name} {user.last_name}")
        print(f"   Activo: {user.is_active}")
        print(f"   Verificado: {user.is_verified}")
        print(f"   Rol: {user.role.name if user.role else 'Sin rol'}")
        print(f"   Intentos fallidos: {user.failed_login_attempts}")
        print(f"   Bloqueado: {user.is_locked()}")
        
        # Verificar si está bloqueado
        if user.is_locked():
            print("❌ Usuario está BLOQUEADO")
            return False
        
        # Verificar si está activo
        if not user.is_active:
            print("❌ Usuario está INACTIVO")
            return False
        
        # Verificar contraseña
        if user.check_password(password):
            print("✅ Contraseña es CORRECTA")
            print("🎉 LOGIN EXITOSO")
            return True
        else:
            print("❌ Contraseña es INCORRECTA")
            return False

if __name__ == "__main__":
    # Probar con el email incorrecto que mencionaste
    print("=" * 60)
    print("PRUEBA 1: Con el email que mencionaste")
    test_login('admin@infomilo.con', 'admin123')
    
    print("\n" + "=" * 60)
    print("PRUEBA 2: Con el email correcto")
    test_login('admin@infomilo.com', 'admin123')
    
    print("\n" + "=" * 60)
    print("PRUEBA 3: Con contraseña incorrecta")
    test_login('admin@infomilo.com', 'wrong123')
