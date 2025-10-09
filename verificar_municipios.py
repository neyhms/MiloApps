#!/usr/bin/env python3
"""
Script para verificar tabla de municipios
"""

import sqlite3
import os

def verificar_tabla_municipios():
    """Verifica la tabla de municipios."""
    
    db_path = os.path.join('data', 'miloapps.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🏛️ VERIFICANDO TABLA MUNICIPIOS")
        print("=" * 40)
        
        # Verificar si existe la tabla
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='talent_municipios'")
        exists = cursor.fetchone()
        
        if exists:
            print("✅ Tabla talent_municipios existe")
            
            # Verificar estructura
            cursor.execute("PRAGMA table_info(talent_municipios)")
            columns = cursor.fetchall()
            print(f"📋 Columnas ({len(columns)}):")
            for col in columns:
                print(f"   - {col[1]}: {col[2]} {'(PK)' if col[5] else ''}")
            
            # Verificar datos
            cursor.execute("SELECT COUNT(*) FROM talent_municipios")
            count = cursor.fetchone()[0]
            print(f"📊 Total registros: {count}")
            
            if count > 0:
                cursor.execute("SELECT id, nombre, departamento FROM talent_municipios LIMIT 5")
                records = cursor.fetchall()
                print("📄 Primeros municipios:")
                for record in records:
                    print(f"   - {record[0]}: {record[1]} - {record[2]}")
        else:
            print("❌ Tabla talent_municipios NO existe")
        
        return exists is not None
        
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
    verificar_tabla_municipios()