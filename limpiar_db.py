#!/usr/bin/env python3
"""
Script para limpiar la base de datos y preparar para el nuevo sistema de entidades
"""

import sqlite3
import os

def limpiar_base_datos():
    """Limpia completamente la base de datos."""
    
    db_path = os.path.join('data', 'miloapps.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🧹 LIMPIANDO BASE DE DATOS")
        print("=" * 30)
        
        # Eliminar todas las tablas talent
        tablas_talent = [
            'talent_prestadores_new',
            'talent_municipios',
            'talent_auditoria'
        ]
        
        for tabla in tablas_talent:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {tabla}")
                print(f"✅ Tabla {tabla} eliminada")
            except sqlite3.Error as e:
                print(f"⚠️ Error eliminando {tabla}: {e}")
        
        conn.commit()
        
        print(f"\n🎉 BASE DE DATOS LIMPIADA")
        print(f"📝 Las tablas serán recreadas automáticamente")
        
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
    limpiar_base_datos()