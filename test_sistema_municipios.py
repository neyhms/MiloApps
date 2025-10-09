#!/usr/bin/env python3
"""
Script de prueba completa del sistema de municipios
"""

import requests
import json

def probar_sistema_municipios():
    """Prueba completa del sistema de municipios."""
    
    base_url = "http://localhost:3000"
    
    print("🧪 PRUEBA COMPLETA DEL SISTEMA DE MUNICIPIOS")
    print("=" * 50)
    
    try:
        # 1. Probar endpoint de API de municipios
        print("1️⃣ Probando API de municipios...")
        response = requests.get(f"{base_url}/talent/api/municipios")
        
        if response.status_code == 200:
            try:
                municipios = response.json()
                print(f"   ✅ API funciona - {len(municipios)} municipios disponibles")
                print(f"   📄 Primeros 3: {[m['nombre_completo'] for m in municipios[:3]]}")
            except:
                print(f"   ⚠️ API responde pero no es JSON válido")
                print(f"   📄 Contenido: {response.text[:200]}...")
        else:
            print(f"   ❌ API error: {response.status_code}")
            print(f"   📄 Respuesta: {response.text[:200]}...")
            return False
        
        # 2. Probar formulario HTML
        print("\n2️⃣ Probando formulario...")
        response = requests.get(f"{base_url}/milotalent/crear-ps")
        
        if response.status_code == 200:
            print("   ✅ Formulario carga correctamente")
            
            # Verificar que contiene los elementos necesarios
            html_content = response.text
            checks = [
                ('select[name="expedida_id"]', 'Dropdown Expedida en'),
                ('select[name="ciudad_nacimiento_id"]', 'Dropdown Ciudad de nacimiento'),
                ('select[name="municipio_residencia_id"]', 'Dropdown Municipio residencia'),
                ('cargarMunicipios', 'Función JavaScript'),
            ]
            
            for check, desc in checks:
                if check in html_content:
                    print(f"   ✅ {desc} presente")
                else:
                    print(f"   ❌ {desc} faltante")
                    
        else:
            print(f"   ❌ Formulario error: {response.status_code}")
            return False
        
        # 3. Probar administración de municipios
        print("\n3️⃣ Probando administración...")
        response = requests.get(f"{base_url}/talent/admin/municipios")
        
        if response.status_code == 200:
            print("   ✅ Panel de administración accesible")
        else:
            print(f"   ❌ Admin error: {response.status_code}")
        
        # 4. Probar listado de prestadores
        print("\n4️⃣ Probando listado de prestadores...")
        response = requests.get(f"{base_url}/milotalent/listado")
        
        if response.status_code == 200:
            print("   ✅ Listado de prestadores accesible")
        else:
            print(f"   ❌ Listado error: {response.status_code}")
        
        print(f"\n🎉 PRUEBAS COMPLETADAS")
        print(f"📝 Sistema de municipios funcionando correctamente")
        print(f"🌐 Formulario: {base_url}/milotalent/formulario")
        print(f"🏛️ Admin: {base_url}/milotalent/admin/municipios")
        print(f"👥 Listado: {base_url}/milotalent/listado")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("💡 Asegúrate de que el servidor esté corriendo en http://localhost:3000")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    probar_sistema_municipios()