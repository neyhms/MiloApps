#!/usr/bin/env python3
"""
Script para probar el endpoint API de verificación de cédula
"""

import requests
import json

def test_api_endpoint():
    """Prueba el endpoint API de verificación de cédula."""
    
    base_url = "http://localhost:3000"
    session = requests.Session()
    
    try:
        print("🔍 PROBANDO ENDPOINT API DE VERIFICACIÓN")
        print("=" * 50)
        
        # 1. Intentar acceder al endpoint sin autenticación
        print("1. Probando sin autenticación...")
        api_url = f"{base_url}/milotalent/api/verificar-cedula?cedula=99999999"
        response = session.get(api_url)
        
        if response.status_code == 302:
            print("   ✅ Endpoint requiere autenticación (correcto)")
        else:
            print(f"   ⚠️  Respuesta inesperada: {response.status_code}")
            
        # 2. Obtener la página de login para el token CSRF
        print("\n2. Obteniendo página de login...")
        login_url = f"{base_url}/auth/login"
        login_response = session.get(login_url)
        
        if login_response.status_code == 200:
            print("   ✅ Página de login obtenida")
        else:
            print(f"   ❌ Error obteniendo login: {login_response.status_code}")
            return False
            
        # 3. Mostrar instrucciones para prueba manual
        print("\n3. 📋 INSTRUCCIONES PARA PRUEBA MANUAL:")
        print("   1. Abre el navegador en: http://localhost:3000/auth/login")
        print("   2. Inicia sesión con usuario válido")
        print("   3. Abre las herramientas de desarrollador (F12)")
        print("   4. Ve a la consola y ejecuta:")
        print("      fetch('/milotalent/api/verificar-cedula?cedula=99999999')")
        print("        .then(r => r.json())")
        print("        .then(d => console.log(d))")
        print("   5. Deberías ver: {existe: true, nombre: 'JUAN CARLOS PÉREZ LÓPEZ', cedula: '99999999'}")
        
        # 4. Probar con cédula que no existe
        print("\n4. Para probar cédula que NO existe:")
        print("   Ejecuta en consola del navegador:")
        print("      fetch('/milotalent/api/verificar-cedula?cedula=11111111')")
        print("        .then(r => r.json())")
        print("        .then(d => console.log(d))")
        print("   5. Deberías ver: {existe: false, cedula: '11111111'}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("   Asegúrate de que el servidor esté ejecutándose en http://localhost:3000")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

def mostrar_javascript_debug():
    """Muestra código JavaScript para debug en el navegador."""
    
    print("\n🔧 CÓDIGO JAVASCRIPT PARA DEBUG EN NAVEGADOR:")
    print("=" * 50)
    
    js_debug = '''
// Función para probar la validación
function probarValidacion(cedula) {
    console.log(`Probando validación para cédula: ${cedula}`);
    
    fetch(`/milotalent/api/verificar-cedula?cedula=${cedula}`)
        .then(response => {
            console.log('Status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Respuesta del servidor:', data);
            if (data.existe) {
                console.log(`✅ DUPLICADO ENCONTRADO - Nombre: ${data.nombre}`);
            } else {
                console.log('✅ CÉDULA DISPONIBLE - Se puede registrar');
            }
        })
        .catch(error => {
            console.error('❌ Error:', error);
        });
}

// Probar cédulas
probarValidacion('99999999'); // Debería encontrar duplicado
probarValidacion('11111111'); // Debería estar disponible
'''
    
    print(js_debug)
    
    print("\n📝 PASOS PARA USAR EL DEBUG:")
    print("1. Inicia sesión en: http://localhost:3000/auth/login")
    print("2. Abre herramientas de desarrollador (F12)")
    print("3. Ve a la pestaña 'Console'")
    print("4. Copia y pega el código JavaScript de arriba")
    print("5. Presiona Enter para ejecutar")
    print("6. Observa los resultados en la consola")

if __name__ == "__main__":
    test_api_endpoint()
    mostrar_javascript_debug()
    
    print("\n🎯 PRUEBA DEL FORMULARIO:")
    print("1. Ve a: http://localhost:3000/milotalent/crear")
    print("2. Llena el formulario con cédula: 99999999")
    print("3. Al enviar, debería mostrar alerta con:")
    print("   'Ya existe un prestador con la cédula 99999999'")
    print("   'Nombre: JUAN CARLOS PÉREZ LÓPEZ'")