#!/usr/bin/env python3
"""Script para agregar la columna profile_picture a la base de datos"""

import sqlite3
import os

def add_profile_picture_column():
    """Agregar columna profile_picture a la tabla users"""
    
    # Ruta de la base de datos
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'miloapps.db')
    
    if not os.path.exists(db_path):
        print("❌ Base de datos no encontrada")
        return False
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'profile_picture' in columns:
            print("✅ La columna 'profile_picture' ya existe")
            conn.close()
            return True
        
        # Agregar la columna
        cursor.execute("ALTER TABLE users ADD COLUMN profile_picture VARCHAR(255)")
        
        # Commit y cerrar
        conn.commit()
        conn.close()
        
        print("✅ Columna 'profile_picture' agregada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al agregar la columna: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Actualizando base de datos...")
    success = add_profile_picture_column()
    if success:
        print("🎉 Base de datos actualizada correctamente")
    else:
        print("💥 Error al actualizar la base de datos")