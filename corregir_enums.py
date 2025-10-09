#!/usr/bin/env python3
"""
Script para corregir todos los valores enum problemáticos
"""

import sqlite3
import os

def corregir_todos_los_enums():
    """Corrige todos los valores enum problemáticos en la base de datos."""
    
    db_path = os.path.join('data', 'miloapps.db')
    
    # Correcciones a aplicar
    correcciones = {
        'discapacidad': {
            'NINGUNA': 'NO'
        },
        'regimen_iva': {
            'COMÚN': 'RESPONSABLE'
        },
        'tipo_riesgo': {
            'CLASE_II': 'II',
            'CLASE_IV': 'IV'
        },
        'nuevo_viejo': {
            'NUEVO': 'N'
        }
    }
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 CORRIGIENDO TODOS LOS VALORES ENUM")
        print("=" * 40)
        
        total_correcciones = 0
        
        for campo, mapeo in correcciones.items():
            print(f"\n📝 Corrigiendo campo: {campo.upper()}")
            
            for valor_incorrecto, valor_correcto in mapeo.items():
                cursor.execute(
                    f"UPDATE talent_prestadores_new SET {campo} = ? WHERE {campo} = ?",
                    (valor_correcto, valor_incorrecto)
                )
                filas_afectadas = cursor.rowcount
                
                if filas_afectadas > 0:
                    print(f"   ✅ '{valor_incorrecto}' -> '{valor_correcto}': {filas_afectadas} registros")
                    total_correcciones += filas_afectadas
                else:
                    print(f"   ➖ '{valor_incorrecto}': No encontrado")
        
        conn.commit()
        
        print(f"\n📊 RESUMEN FINAL:")
        print(f"   - Total correcciones aplicadas: {total_correcciones}")
        
        # Verificar que todo está correcto ahora
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
        
        problemas_restantes = 0
        print(f"\n🔍 VERIFICACIÓN FINAL:")
        
        for campo, valores_esperados in campos_enum.items():
            cursor.execute(f"SELECT DISTINCT {campo} FROM talent_prestadores_new WHERE {campo} IS NOT NULL")
            valores_db = [row[0] for row in cursor.fetchall()]
            valores_problematicos = [v for v in valores_db if v not in valores_esperados]
            
            if valores_problematicos:
                print(f"   ❌ {campo.upper()}: {valores_problematicos}")
                problemas_restantes += len(valores_problematicos)
            else:
                print(f"   ✅ {campo.upper()}: OK")
        
        if problemas_restantes == 0:
            print(f"\n🎉 TODOS LOS ENUMS CORREGIDOS EXITOSAMENTE")
            print(f"📝 No más errores LookupError esperados")
        else:
            print(f"\n⚠️ Aún quedan {problemas_restantes} problemas")
        
        return problemas_restantes == 0
        
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
    corregir_todos_los_enums()