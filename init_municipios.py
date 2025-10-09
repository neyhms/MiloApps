#!/usr/bin/env python3
"""
Script para crear municipios iniciales de Colombia
"""

import sqlite3
from datetime import datetime
import os

def crear_municipios_iniciales():
    """Crea municipios principales de Colombia."""
    
    db_path = os.path.join('data', 'miloapps.db')
    
    # Lista de municipios principales
    municipios = [
        ('BOGOTÁ', 'CUNDINAMARCA', '11001'),
        ('MEDELLÍN', 'ANTIOQUIA', '05001'),
        ('CALI', 'VALLE DEL CAUCA', '76001'),
        ('BARRANQUILLA', 'ATLÁNTICO', '08001'),
        ('CARTAGENA', 'BOLÍVAR', '13001'),
        ('BUCARAMANGA', 'SANTANDER', '68001'),
        ('PEREIRA', 'RISARALDA', '66001'),
        ('MANIZALES', 'CALDAS', '17001'),
        ('IBAGUÉ', 'TOLIMA', '73001'),
        ('NEIVA', 'HUILA', '41001'),
        ('VILLAVICENCIO', 'META', '50001'),
        ('PASTO', 'NARIÑO', '52001'),
        ('MONTERÍA', 'CÓRDOBA', '23001'),
        ('POPAYÁN', 'CAUCA', '19001'),
        ('SANTA MARTA', 'MAGDALENA', '47001'),
        ('CÚCUTA', 'NORTE DE SANTANDER', '54001'),
        ('ARMENIA', 'QUINDÍO', '63001'),
        ('TUNJA', 'BOYACÁ', '15001'),
        ('FLORENCIA', 'CAQUETÁ', '18001'),
        ('VALLEDUPAR', 'CESAR', '20001')
    ]
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si la tabla existe
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='talent_municipios'
        """)
        
        if not cursor.fetchone():
            print("❌ La tabla talent_municipios no existe")
            print("   Ejecuta el servidor para crear las tablas primero")
            return False
        
        insertados = 0
        duplicados = 0
        
        for nombre, departamento, codigo_dane in municipios:
            nombre_completo = f"{nombre} - {departamento}"
            
            # Verificar si ya existe
            cursor.execute("""
                SELECT id FROM talent_municipios 
                WHERE nombre_completo = ?
            """, (nombre_completo,))
            
            if cursor.fetchone():
                duplicados += 1
                continue
            
            # Insertar municipio
            cursor.execute("""
                INSERT INTO talent_municipios (
                    nombre, departamento, codigo_dane, nombre_completo, 
                    activo, fecha_creacion, usuario_creacion
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                nombre,
                departamento,
                codigo_dane,
                nombre_completo,
                True,
                datetime.now().isoformat(),
                'SYSTEM'
            ))
            
            insertados += 1
        
        conn.commit()
        
        print(f"✅ Municipios creados exitosamente:")
        print(f"   - Insertados: {insertados}")
        print(f"   - Ya existían: {duplicados}")
        print(f"   - Total procesados: {len(municipios)}")
        
        # Verificar total
        cursor.execute("SELECT COUNT(*) FROM talent_municipios")
        total = cursor.fetchone()[0]
        print(f"📊 Total municipios en BD: {total}")
        
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
    print("🏛️ CREANDO MUNICIPIOS INICIALES DE COLOMBIA")
    print("=" * 50)
    
    resultado = crear_municipios_iniciales()
    
    if resultado:
        print("\n🎯 LISTO PARA USAR:")
        print("1. Ve a: http://localhost:3000/milotalent/dashboard")
        print("2. Haz clic en 'Administrar Municipios'")
        print("3. Verás los municipios principales ya creados")
        print("4. Puedes agregar más municipios según necesites")
    else:
        print("\n❌ No se pudieron crear los municipios iniciales")
        print("   Asegúrate de que el servidor haya ejecutado al menos una vez")