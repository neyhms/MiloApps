#!/usr/bin/env python3
"""
Script para probar POST completo con todos los campos requeridos
"""

import requests
from datetime import date

# URL del endpoint
url = "http://localhost:3000/milotalent/crear-ps"

# Datos completos del formulario
data = {
    # IDENTIFICACIÓN
    'cedula_ps': '1234567890',
    'expedida': 'CALI (VAL)',
    'sexo': 'M',
    'nombre_1': 'Juan',
    'nombre_2': 'Carlos',
    'apellido_1': 'Pérez',
    'apellido_2': 'López',
    
    # NACIMIENTO
    'fecha_nacimiento': '1990-01-15',
    'ciudad_nacimiento': 'CALI (VAL)',
    'pais_nacimiento': 'CO',
    
    # CONTACTO Y RESIDENCIA
    'direccion': 'CL. 24 A # 16 -47',
    'municipio_residencia': 'JAMUNDI (VAL)',
    'pais_residencia': 'CO',
    'telefono': '3174299552',
    'mail': 'juan.perez@ejemplo.com',
    
    # INFORMACIÓN PERSONAL
    'profesion': 'CONTADOR PÚBLICO',
    'estado_civil': 'Soltero',
    'no_hijos': '0',
    'rh': 'O+',
    'discapacidad': 'NINGUNA',
    'identidad_genero': 'MASCULINO',
    'raza': 'MESTIZO',
    
    # INFORMACIÓN BANCARIA
    'banco': 'BANCOLOMBIA',
    'cuenta_bancaria': '131-90620-3',
    'tipo_cuenta': '02 Cuenta de Ahorros',
    
    # SEGURIDAD SOCIAL
    'regimen_iva': '98 RUT Régimen Simplificado',
    'eps': 'SUSALUD - SURA - SURAMERICANA E.P.S.',
    'afp': 'PORVENIR',
    'arl': 'POSITIVA ARL',
    'tipo_riesgo': '001 Labores administrativas Clase I',
    'caja': 'COMFENALCO',
    'operador_ss': 'APORTES EN LINEA',
    
    # INFORMACIÓN DEL SISTEMA
    'codigo_sap': '1000698',
    'nuevo_viejo': 'N',
    'area_personal': 'PS'
}

print("=== ENVIANDO POST COMPLETO ===")
print(f"URL: {url}")
print(f"Datos: {len(data)} campos")

try:
    response = requests.post(url, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Content Length: {len(response.text)}")
    
    if response.status_code == 200:
        print("✅ ¡POST EXITOSO!")
        if "éxito" in response.text.lower() or "creado" in response.text.lower():
            print("✅ PS creado exitosamente")
        else:
            print("⚠️  Respuesta exitosa pero sin mensaje de confirmación")
    else:
        print(f"❌ Error {response.status_code}")
        # Solo mostrar primeros 500 caracteres del error
        print(f"Respuesta: {response.text[:500]}...")

except Exception as e:
    print(f"❌ Error de conexión: {e}")