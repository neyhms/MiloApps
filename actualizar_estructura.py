#!/usr/bin/env python3
"""
Script para actualizar la estructura de la tabla talent_prestadores_new
agregando las columnas de referencias a municipios
"""

import sqlite3
import os

def actualizar_estructura_tabla():
    """Actualiza la estructura de la tabla agregando columnas de municipios."""
    
    db_path = os.path.join('data', 'miloapps.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 ACTUALIZANDO ESTRUCTURA DE TABLA")
        print("=" * 40)
        
        # Verificar columnas existentes
        cursor.execute("PRAGMA table_info(talent_prestadores_new)")
        columns = [col[1] for col in cursor.fetchall()]
        
        print(f"📋 Columnas actuales: {len(columns)}")
        
        # Columnas a agregar
        nuevas_columnas = [
            ("expedida_id", "INTEGER"),
            ("ciudad_nacimiento_id", "INTEGER"),
            ("municipio_residencia_id", "INTEGER")
        ]
        
        agregadas = 0
        
        for columna, tipo in nuevas_columnas:
            if columna not in columns:
                try:
                    cursor.execute(f"ALTER TABLE talent_prestadores_new ADD COLUMN {columna} {tipo}")
                    print(f"✅ Agregada columna: {columna}")
                    agregadas += 1
                except sqlite3.Error as e:
                    print(f"❌ Error agregando {columna}: {e}")
            else:
                print(f"⚠️  Columna {columna} ya existe")
        
        conn.commit()
        
        print(f"\n📊 RESUMEN:")
        print(f"   - Columnas agregadas: {agregadas}")
        print(f"   - Total columnas ahora: {len(columns) + agregadas}")
        
        # Verificar estructura final
        cursor.execute("PRAGMA table_info(talent_prestadores_new)")
        nuevas_columns = [col[1] for col in cursor.fetchall()]
        
        municipios_cols = [col for col in nuevas_columns if 'municipio' in col or 'expedida_id' in col or 'ciudad_nacimiento_id' in col]
        print(f"🏛️ Columnas de municipios: {municipios_cols}")
        
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
    print("🔧 ACTUALIZACIÓN DE ESTRUCTURA - TABLA PRESTADORES")
    print("=" * 55)
    
    resultado = actualizar_estructura_tabla()
    
    if resultado:
        print("\n🎉 ESTRUCTURA ACTUALIZADA EXITOSAMENTE")
        print("📝 Ahora puedes ejecutar la migración de datos")
        print("💡 Comando: python migrar_municipios.py")
    else:
        print("\n❌ Error actualizando estructura")