#!/usr/bin/env python3
"""
Script para verificar que el sistema de entidades esté funcionando correctamente
"""

import requests
import sys

def verificar_sistema():
    """Verifica todos los componentes del sistema"""
    
    base_url = "http://localhost:3000"
    
    print("🔍 VERIFICACIÓN DEL SISTEMA DE ENTIDADES")
    print("=" * 50)
    
    errores = []
    exitos = []
    
    # Verificar API de entidades
    apis_test = [
        ("Municipios", "/admin/entidades/api/municipio"),
        ("Profesiones", "/admin/entidades/api/profesion"),
        ("Bancos", "/admin/entidades/api/banco"),
        ("EPS", "/admin/entidades/api/eps"),
        ("AFP", "/admin/entidades/api/afp"),
        ("ARL", "/admin/entidades/api/arl"),
        ("Cajas Compensación", "/admin/entidades/api/caja_compensacion"),
        ("Operadores SS", "/admin/entidades/api/operador_ss"),
        ("Áreas Personal", "/admin/entidades/api/area_personal"),
        ("Todas las entidades", "/admin/entidades/api/all"),
    ]
    
    for nombre, endpoint in apis_test:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    count = len(data.get('data', []))
                    exitos.append(f"✅ {nombre}: {count} registros")
                else:
                    errores.append(f"❌ {nombre}: {data.get('error', 'Error desconocido')}")
            else:
                errores.append(f"❌ {nombre}: HTTP {response.status_code}")
                
        except requests.RequestException as e:
            errores.append(f"❌ {nombre}: Error de conexión - {e}")
        except Exception as e:
            errores.append(f"❌ {nombre}: {e}")
    
    # Verificar endpoints principales del sistema
    endpoints_principales = [
        ("Dashboard", "/dashboard"),
        ("Status API", "/api/status"),
        ("MiloTalent Dashboard", "/milotalent/"),
        ("MiloTalent Formulario", "/milotalent/crear-ps"),
        ("MiloTalent Listado", "/milotalent/listado-ps"),
    ]
    
    print("\n🌐 VERIFICACIÓN DE ENDPOINTS PRINCIPALES:")
    
    for nombre, endpoint in endpoints_principales:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                exitos.append(f"✅ {nombre}: 200 OK")
            elif response.status_code == 302:
                exitos.append(f"✅ {nombre}: 302 Redirect (normal)")
            else:
                errores.append(f"❌ {nombre}: HTTP {response.status_code}")
                
        except requests.RequestException as e:
            errores.append(f"❌ {nombre}: Error de conexión - {e}")
    
    # Mostrar resultados
    print("\n📊 RESULTADOS:")
    print("-" * 30)
    
    if exitos:
        print("\n🎉 ÉXITOS:")
        for exito in exitos:
            print(f"   {exito}")
    
    if errores:
        print("\n⚠️  ERRORES:")
        for error in errores:
            print(f"   {error}")
    
    # Resumen final
    total_tests = len(apis_test) + len(endpoints_principales)
    total_exitos = len(exitos)
    total_errores = len(errores)
    
    print(f"\n📈 RESUMEN:")
    print(f"   Total de pruebas: {total_tests}")
    print(f"   Exitosas: {total_exitos}")
    print(f"   Con errores: {total_errores}")
    
    if total_errores == 0:
        print("\n🚀 SISTEMA COMPLETAMENTE FUNCIONAL")
        return True
    else:
        print(f"\n⚠️  SISTEMA CON {total_errores} ERRORES")
        return False

if __name__ == "__main__":
    try:
        resultado = verificar_sistema()
        sys.exit(0 if resultado else 1)
    except KeyboardInterrupt:
        print("\n❌ Verificación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)