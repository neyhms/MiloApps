#!/usr/bin/env python3
"""
Script para insertar un registro de prueba directamente en la base de datos
"""

import sqlite3
from datetime import datetime
import os

def insertar_registro_prueba():
    """Inserta un registro de prueba en la base de datos."""
    
    db_path = os.path.join('data', 'miloapps.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada en: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si ya existe
        cursor.execute("SELECT * FROM talent_prestadores_new WHERE cedula_ps = ?", ('12345678',))
        existing = cursor.fetchone()
        
        if existing:
            print("✅ Ya existe un prestador con cédula 12345678")
            print(f"   Nombre: {existing[2]} {existing[3]}")  # nombres_ps, apellidos_ps
            return True
        
        # Insertar registro de prueba
        cursor.execute("""
            INSERT INTO talent_prestadores_new (
                cedula_ps, nombres_ps, apellidos_ps, fecha_nacimiento, 
                sexo, estado_civil, telefono, email, direccion, 
                codigo_sap, usuario_registro, fecha_registro
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            '12345678',
            'Juan Carlos',
            'Pérez López',
            '1990-01-15',
            'M',
            'S',
            '+57 300 123 4567',
            'juan.perez.test@example.com',
            'Calle 123 #45-67',
            'SAP12345678',
            'TEST_SYSTEM',
            datetime.now().isoformat()
        ))
        
        conn.commit()
        print("✅ Registro de prueba insertado exitosamente")
        print("   Cédula: 12345678")
        print("   Nombre: Juan Carlos Pérez López")
        
        # Verificar total de registros
        cursor.execute("SELECT COUNT(*) FROM talent_prestadores_new")
        total = cursor.fetchone()[0]
        print(f"📊 Total prestadores en BD: {total}")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Error con la base de datos: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🔧 INSERTANDO REGISTRO DE PRUEBA PARA VALIDACIÓN DE UNICIDAD")
    print("=" * 60)
    
    resultado = insertar_registro_prueba()
    
    if resultado:
        print("\n🎯 AHORA PUEDES PROBAR:")
        print("1. Ve a: http://localhost:3000/milotalent/crear")
        print("2. Llena el formulario con cédula: 12345678")
        print("3. Al enviar debería mostrar la alerta de duplicado")
        print("4. Verifica que el JavaScript intercepte y muestre el mensaje")
    else:
        print("\n❌ No se pudo insertar el registro de prueba")