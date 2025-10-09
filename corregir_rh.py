#!/usr/bin/env python3
"""
Script para corregir los valores RH en la base de datos
"""

import sqlite3
import os

def corregir_valores_rh():
    """Corrige los valores de RH en la base de datos para que coincidan con el enum."""
    
    db_path = os.path.join('data', 'miloapps.db')
    
    # Mapeo de valores incorrectos a valores correctos
    correcciones = {
        'O_POSITIVO': 'O+',  # Nombre del enum -> Valor del enum
        'A_POSITIVO': 'A+',
        'A_NEGATIVO': 'A-',
        'B_POSITIVO': 'B+',
        'B_NEGATIVO': 'B-',
        'AB_POSITIVO': 'AB+',
        'AB_NEGATIVO': 'AB-',
        'O_NEGATIVO': 'O-'
    }
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🩸 CORRIGIENDO VALORES RH")
        print("=" * 30)
        
        # Verificar valores actuales
        cursor.execute("SELECT DISTINCT rh FROM talent_prestadores_new WHERE rh IS NOT NULL")
        valores_actuales = [row[0] for row in cursor.fetchall()]
        print(f"📋 Valores encontrados: {valores_actuales}")
        
        correcciones_aplicadas = 0
        
        for valor_incorrecto, valor_correcto in correcciones.items():
            if valor_incorrecto in valores_actuales:
                cursor.execute(
                    "UPDATE talent_prestadores_new SET rh = ? WHERE rh = ?",
                    (valor_correcto, valor_incorrecto)
                )
                filas_afectadas = cursor.rowcount
                if filas_afectadas > 0:
                    print(f"✅ '{valor_incorrecto}' -> '{valor_correcto}': {filas_afectadas} registros")
                    correcciones_aplicadas += filas_afectadas
        
        conn.commit()
        
        # Verificar resultados
        cursor.execute("SELECT DISTINCT rh FROM talent_prestadores_new WHERE rh IS NOT NULL")
        valores_finales = [row[0] for row in cursor.fetchall()]
        
        print(f"\n📊 RESUMEN:")
        print(f"   - Correcciones aplicadas: {correcciones_aplicadas}")
        print(f"   - Valores finales: {valores_finales}")
        
        # Mostrar registros corregidos
        cursor.execute("SELECT id, nombre_1, apellido_1, rh FROM talent_prestadores_new")
        registros = cursor.fetchall()
        
        print(f"\n👥 REGISTROS CORREGIDOS:")
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
    corregir_valores_rh()