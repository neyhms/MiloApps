#!/usr/bin/env python3
"""
Script para verificar los valores RH en la base de datos
"""

import sqlite3
import os

def verificar_valores_rh():
    """Verifica los valores de RH almacenados en la base de datos."""
    
    db_path = os.path.join('data', 'miloapps.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🩸 VERIFICANDO VALORES RH EN BASE DE DATOS")
        print("=" * 45)
        
        # Verificar valores únicos de RH
        cursor.execute("SELECT DISTINCT rh FROM talent_prestadores_new WHERE rh IS NOT NULL")
        valores_rh = [row[0] for row in cursor.fetchall()]
        
        print(f"📋 Valores RH encontrados: {len(valores_rh)}")
        for valor in valores_rh:
            print(f"   - '{valor}' (tipo: {type(valor).__name__})")
        
        # Verificar registros específicos con problemas
        cursor.execute("SELECT id, nombre_1, apellido_1, rh FROM talent_prestadores_new")
        registros = cursor.fetchall()
        
        print(f"\n👥 REGISTROS COMPLETOS:")
        for registro in registros:
            print(f"   ID {registro[0]}: {registro[1]} {registro[2]} - RH: '{registro[3]}'")
        
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
    verificar_valores_rh()