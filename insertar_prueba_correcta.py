#!/usr/bin/env python3
"""
Script para insertar un registro de prueba con la estructura correcta
"""

import sqlite3
from datetime import datetime
import os

def insertar_registro_correcto():
    """Inserta un registro de prueba con la estructura correcta."""
    
    db_path = os.path.join('data', 'miloapps.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si ya existe la cédula de prueba
        cursor.execute("SELECT * FROM talent_prestadores_new WHERE cedula_ps = ?", ('99999999',))
        existing = cursor.fetchone()
        
        if existing:
            print("✅ Ya existe un prestador con cédula 99999999")
            print(f"   Nombre: {existing[3]} {existing[5]}")  # nombre_1, apellido_1
            return True
        
        # Insertar registro de prueba
        cursor.execute("""
            INSERT INTO talent_prestadores_new (
                cedula_ps, expedida, nombre_1, nombre_2, apellido_1, apellido_2,
                sexo, codigo_sap, fecha_nacimiento, ciudad_nacimiento, pais_nacimiento,
                direccion, pais_residencia, municipio_residencia, telefono, mail,
                profesion, estado_civil, no_hijos, rh, discapacidad, identidad_genero,
                raza, banco, cuenta_bancaria, tipo_cuenta, regimen_iva, eps, afp, arl,
                tipo_riesgo, caja, operador_ss, nuevo_viejo, area_personal,
                fecha_registro, usuario_registro
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            '99999999',           # cedula_ps
            'BOGOTÁ',            # expedida
            'JUAN',              # nombre_1
            'CARLOS',            # nombre_2
            'PÉREZ',             # apellido_1
            'LÓPEZ',             # apellido_2
            'M',                 # sexo
            'SAP99999999',       # codigo_sap
            '1990-01-15',        # fecha_nacimiento
            'BOGOTÁ',            # ciudad_nacimiento
            'COLOMBIA',          # pais_nacimiento
            'CALLE 123 #45-67',  # direccion
            'COLOMBIA',          # pais_residencia
            'BOGOTÁ',            # municipio_residencia
            '+57 300 123 4567',  # telefono
            'juan.test@test.com', # mail
            'INGENIERO',         # profesion
            'SOLTERO',           # estado_civil
            0,                   # no_hijos
            'O+',                # rh
            'NINGUNA',           # discapacidad
            'MASCULINO',         # identidad_genero
            'MESTIZO',           # raza
            'BANCOLOMBIA',       # banco
            '12345678901',       # cuenta_bancaria
            'AHORROS',           # tipo_cuenta
            'COMÚN',             # regimen_iva
            'SURA',              # eps
            'PROTECCIÓN',        # afp
            'SURA',              # arl
            'I',                 # tipo_riesgo
            'COMPENSAR',         # caja
            'SURA',              # operador_ss
            'NUEVO',             # nuevo_viejo
            'DESARROLLO',        # area_personal
            datetime.now().isoformat(),  # fecha_registro
            'TEST_SYSTEM'        # usuario_registro
        ))
        
        conn.commit()
        print("✅ Registro de prueba insertado exitosamente")
        print("   Cédula: 99999999")
        print("   Nombre: JUAN CARLOS PÉREZ LÓPEZ")
        
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
    print("🔧 INSERTANDO REGISTRO DE PRUEBA (ESTRUCTURA CORRECTA)")
    print("=" * 60)
    
    resultado = insertar_registro_correcto()
    
    if resultado:
        print("\n🎯 AHORA PUEDES PROBAR LA VALIDACIÓN:")
        print("1. Ve a: http://localhost:3000/milotalent/crear")
        print("2. Inicia sesión si es necesario")
        print("3. Llena el formulario con cédula: 99999999")
        print("4. Al enviar debería mostrar la alerta de duplicado")
        print("5. Mensaje esperado: 'Ya existe un prestador con la cédula 99999999'")
        print("6. Nombre: JUAN CARLOS PÉREZ LÓPEZ")
    else:
        print("\n❌ No se pudo insertar el registro de prueba")