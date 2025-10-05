#!/usr/bin/env python3
"""
Script para agregar el campo bio a la tabla users
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from models import db, User, init_db
from flask import Flask
import sqlite3

def update_database():
    """Agregar columna bio a la tabla users"""
    
    # Configurar Flask app temporal
    app = Flask(__name__)
    
    # Configuración básica
    app.config['SECRET_KEY'] = 'temp-key-for-db-update'
    
    # Base de datos SQLite
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'infomilo.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    print(f"🔍 Actualizando base de datos: {db_path}")
    
    try:
        # Conectar directamente con SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si la columna bio ya existe
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'bio' in columns:
            print("✅ La columna 'bio' ya existe en la tabla users")
        else:
            print("🔧 Agregando columna 'bio' a la tabla users...")
            cursor.execute("ALTER TABLE users ADD COLUMN bio TEXT")
            conn.commit()
            print("✅ Columna 'bio' agregada exitosamente")
        
        # Verificar la estructura actualizada
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        print("📋 Estructura actual de la tabla users:")
        for column in columns:
            print(f"   - {column[1]} ({column[2]})")
        
        conn.close()
        
        # Verificar con SQLAlchemy
        init_db(app)
        
        with app.app_context():
            # Crear todas las tablas (no afecta las existentes)
            db.create_all()
            
            # Verificar que podemos acceder al campo bio
            user = User.query.first()
            if user:
                print(f"✅ Usuario de prueba: {user.username}")
                print(f"   Bio actual: {user.bio or 'No definida'}")
            else:
                print("📋 No hay usuarios en la base de datos")
        
        print("🎉 Actualización de base de datos completada")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando base de datos: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    success = update_database()
    if success:
        print("\n✅ La base de datos está lista para usar el campo 'bio'")
    else:
        print("\n❌ Error en la actualización de la base de datos")
        sys.exit(1)
