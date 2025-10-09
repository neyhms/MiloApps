#!/usr/bin/env python3
"""
Script para verificar la estructura de la tabla y datos existentes
"""

import sqlite3
import os

def verificar_estructura():
    """Verifica la estructura de la tabla."""
    
    db_path = os.path.join('data', 'miloapps.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada en: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Obtener información de la tabla
        cursor.execute("PRAGMA table_info(talent_prestadores_new)")
        columns = cursor.fetchall()
        
        if not columns:
            print("❌ La tabla talent_prestadores_new no existe")
            # Ver qué tablas existen
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print("📋 Tablas existentes:")
            for table in tables:
                print(f"   - {table[0]}")
            return False
        
        print("📋 ESTRUCTURA DE LA TABLA talent_prestadores_new:")
        print("-" * 50)
        for col in columns:
            print(f"   {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'} - {'PK' if col[5] else ''}")
        
        # Verificar registros existentes
        cursor.execute("SELECT COUNT(*) FROM talent_prestadores_new")
        total = cursor.fetchone()[0]
        print(f"\n📊 Total registros: {total}")
        
        if total > 0:
            # Mostrar algunos registros
            cursor.execute("SELECT * FROM talent_prestadores_new LIMIT 3")
            records = cursor.fetchall()
            print("\n📄 Primeros registros:")
            for i, record in enumerate(records):
                print(f"   Registro {i+1}: {record[:5]}...")  # Primeros 5 campos
        
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
    print("🔍 VERIFICANDO ESTRUCTURA DE LA BASE DE DATOS")
    print("=" * 50)
    
    verificar_estructura()