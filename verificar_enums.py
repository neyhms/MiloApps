#!/usr/bin/env python3
"""
Script para verificar todos los campos enum en la base de datos
"""

import sqlite3
import os

def verificar_todos_los_enums():
    """Verifica todos los campos que usan enums para detectar problemas similares."""
    
    db_path = os.path.join('data', 'miloapps.db')
    
    # Campos enum a verificar
    campos_enum = {
        'sexo': ['M', 'F'],
        'estado_civil': ['SOLTERO', 'CASADO', 'UNION_LIBRE', 'DIVORCIADO', 'VIUDO'],
        'rh': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
        'discapacidad': ['SI', 'NO'],
        'identidad_genero': ['MASCULINO', 'FEMENINO', 'NO_BINARIO', 'OTRO'],
        'raza': ['MESTIZO', 'AFRODESCENDIENTE', 'INDÍGENA', 'BLANCO', 'OTRO'],
        'tipo_cuenta': ['AHORROS', 'CORRIENTE'],
        'regimen_iva': ['SIMPLIFICADO', 'RESPONSABLE'],
        'tipo_riesgo': ['I', 'II', 'III', 'IV', 'V'],
        'nuevo_viejo': ['N', 'V']
    }
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 VERIFICANDO TODOS LOS CAMPOS ENUM")
        print("=" * 40)
        
        problemas_encontrados = 0
        
        for campo, valores_esperados in campos_enum.items():
            cursor.execute(f"SELECT DISTINCT {campo} FROM talent_prestadores_new WHERE {campo} IS NOT NULL")
            valores_db = [row[0] for row in cursor.fetchall()]
            
            valores_problematicos = [v for v in valores_db if v not in valores_esperados]
            
            if valores_problematicos:
                print(f"❌ {campo.upper()}: {valores_problematicos} (problemas)")
                problemas_encontrados += len(valores_problematicos)
            else:
                print(f"✅ {campo.upper()}: OK ({len(valores_db)} valores)")
        
        print(f"\n📊 RESUMEN:")
        if problemas_encontrados == 0:
            print(f"✅ Todos los campos enum están correctos")
            print(f"🎉 No hay más problemas de LookupError")
        else:
            print(f"⚠️ Se encontraron {problemas_encontrados} valores problemáticos")
            print(f"💡 Pueden necesitar corrección manual")
        
        return problemas_encontrados == 0
        
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
    verificar_todos_los_enums()