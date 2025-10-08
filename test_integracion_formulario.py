#!/usr/bin/env python3
"""
Prueba de integración del formulario con el sistema de entidades
"""

import requests
import json
from datetime import datetime

def test_api_all_entities():
    """Probar endpoint de todas las entidades"""
    url = "http://localhost:3000/admin/entidades/api/all"
    
    try:
        response = requests.get(url)
        print(f"🌐 GET {url}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print("   ✅ Respuesta exitosa")
                entidades = data.get('data', {})
                
                print("\n📋 ENTIDADES DISPONIBLES:")
                for tipo, lista in entidades.items():
                    print(f"   🔹 {tipo}: {len(lista)} registros")
                    if lista:  # Si hay registros, mostrar el primero como ejemplo
                        primer_item = lista[0]
                        print(f"      Ejemplo: {primer_item}")
                
                # Verificar que tenemos todos los tipos esperados
                tipos_esperados = [
                    'municipio', 'profesion', 'banco', 'eps', 
                    'afp', 'arl', 'caja_compensacion', 
                    'operador_ss', 'area_personal'
                ]
                
                tipos_disponibles = set(entidades.keys())
                tipos_faltantes = set(tipos_esperados) - tipos_disponibles
                
                if tipos_faltantes:
                    print(f"\n⚠️  TIPOS FALTANTES: {tipos_faltantes}")
                else:
                    print("\n✅ TODOS LOS TIPOS DISPONIBLES")
                
                return True
            else:
                print(f"   ❌ Error en respuesta: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def test_individual_apis():
    """Probar endpoints individuales"""
    tipos = [
        'municipio', 'profesion', 'banco', 'eps', 
        'afp', 'arl', 'caja_compensacion', 
        'operador_ss', 'area_personal'
    ]
    
    print("\n🔍 VERIFICACIÓN DE ENDPOINTS INDIVIDUALES:")
    
    resultados = []
    
    for tipo in tipos:
        url = f"http://localhost:3000/admin/entidades/api/{tipo}"
        
        try:
            response = requests.get(url)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                count = len(data.get('data', []))
                print(f"   ✅ {tipo}: {count} registros")
                resultados.append((tipo, True, count))
            else:
                print(f"   ❌ {tipo}: HTTP {response.status_code}")
                resultados.append((tipo, False, 0))
                
        except Exception as e:
            print(f"   ❌ {tipo}: {e}")
            resultados.append((tipo, False, 0))
    
    return resultados

def test_formulario_access():
    """Verificar acceso al formulario"""
    url = "http://localhost:3000/milotalent/crear-ps"
    
    try:
        response = requests.get(url, allow_redirects=False)
        print(f"\n🌐 GET {url}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 302:
            location = response.headers.get('Location', '')
            if '/auth/login' in location:
                print("   ℹ️  Redirige a login (comportamiento esperado)")
                return True
            else:
                print(f"   ⚠️  Redirige a: {location}")
                return False
        elif response.status_code == 200:
            print("   ✅ Acceso directo al formulario")
            return True
        else:
            print(f"   ❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def main():
    print("🧪 PRUEBA DE INTEGRACIÓN DEL FORMULARIO")
    print("=" * 50)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Prueba 1: API de todas las entidades
    print("\n1️⃣  PRUEBA API CONSOLIDADA:")
    api_all_ok = test_api_all_entities()
    
    # Prueba 2: APIs individuales
    print("\n2️⃣  PRUEBA APIS INDIVIDUALES:")
    individual_results = test_individual_apis()
    
    # Prueba 3: Acceso al formulario
    print("\n3️⃣  PRUEBA ACCESO AL FORMULARIO:")
    formulario_ok = test_formulario_access()
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS:")
    
    individual_ok = sum(1 for _, success, _ in individual_results if success)
    individual_total = len(individual_results)
    
    print(f"   🌐 API Consolidada: {'✅' if api_all_ok else '❌'}")
    print(f"   🔗 APIs Individuales: {individual_ok}/{individual_total}")
    print(f"   📄 Acceso Formulario: {'✅' if formulario_ok else '❌'}")
    
    if api_all_ok and individual_ok == individual_total and formulario_ok:
        print("\n🎉 INTEGRACIÓN COMPLETAMENTE FUNCIONAL")
        print("   El formulario debería cargar todos los dropdowns correctamente")
    else:
        print("\n⚠️  HAY PROBLEMAS EN LA INTEGRACIÓN")
        print("   Revisar los errores arriba")
    
    print("\n💡 SIGUIENTE PASO:")
    print("   Ir a http://localhost:3000/milotalent/crear-ps")
    print("   Iniciar sesión y verificar que los dropdowns se cargan")

if __name__ == "__main__":
    main()