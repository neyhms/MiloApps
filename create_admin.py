#!/usr/bin/env python3
"""
Script para verificar y crear usuario administrador
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from models import db, User, Role, init_db
from flask import Flask

def create_admin_user():
    """Crear o verificar usuario administrador"""
    
    # Configurar Flask app temporal
    app = Flask(__name__)
    
    # Configuración básica
    app.config['SECRET_KEY'] = 'temp-key-for-admin-creation'
    
    # Base de datos SQLite
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'infomilo.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar base de datos
    init_db(app)
    
    with app.app_context():
        print("🔍 Verificando usuario administrador...")
        
        # Buscar usuario admin
        admin_user = User.query.filter_by(email='admin@infomilo.com').first()
        
        if admin_user:
            print(f"✅ Usuario admin encontrado:")
            print(f"   Email: {admin_user.email}")
            print(f"   Nombre: {admin_user.first_name} {admin_user.last_name}")
            print(f"   Activo: {admin_user.is_active}")
            print(f"   Rol: {admin_user.role.name if admin_user.role else 'Sin rol'}")
            print(f"   Intentos fallidos: {admin_user.failed_login_attempts}")
            print(f"   Bloqueado: {admin_user.is_locked()}")
            
            # Verificar contraseña
            if admin_user.check_password('admin123'):
                print("✅ Contraseña 'admin123' es correcta")
            else:
                print("❌ Contraseña 'admin123' NO es correcta")
                print("🔧 Actualizando contraseña...")
                admin_user.set_password('admin123')
                admin_user.failed_login_attempts = 0
                admin_user.locked_until = None
                db.session.commit()
                print("✅ Contraseña actualizada a 'admin123'")
            
            # Asegurar que esté activo y desbloqueado
            if not admin_user.is_active:
                admin_user.is_active = True
                db.session.commit()
                print("✅ Usuario activado")
            
            if admin_user.is_locked():
                admin_user.unlock_account()
                db.session.commit()
                print("✅ Usuario desbloqueado")
                
        else:
            print("❌ Usuario admin no encontrado. Creando...")
            
            # Buscar rol admin
            admin_role = Role.query.filter_by(name='admin').first()
            if not admin_role:
                print("🔧 Creando rol admin...")
                admin_role = Role(
                    name='admin',
                    description='Administrador del sistema'
                )
                db.session.add(admin_role)
                db.session.commit()
                print("✅ Rol admin creado")
            
            # Crear usuario admin
            admin_user = User(
                email='admin@infomilo.com',
                username='admin',
                first_name='Admin',
                last_name='InfoMilo',
                phone='',
                company='InfoMilo',
                department='Administración',
                role_id=admin_role.id,
                is_active=True,
                is_verified=True
            )
            admin_user.set_password('admin123')
            
            db.session.add(admin_user)
            db.session.commit()
            
            print("✅ Usuario admin creado exitosamente:")
            print(f"   Email: admin@infomilo.com")
            print(f"   Contraseña: admin123")
            print(f"   Rol: admin")
        
        # Mostrar todos los usuarios
        print("\n📋 Todos los usuarios en la base de datos:")
        users = User.query.all()
        for user in users:
            print(f"   - {user.email} ({user.first_name} {user.last_name}) - Rol: {user.role.name if user.role else 'Sin rol'}")
        
        print(f"\n✅ Total de usuarios: {len(users)}")

if __name__ == "__main__":
    create_admin_user()
