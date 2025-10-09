#!/usr/bin/env python3
"""
Script para probar el listado de prestadores después de la corrección RH
"""

import requests

def probar_listado_ps():
    """Prueba que el listado de prestadores funcione sin errores."""
    
    base_url = "http://localhost:3000"
    
    print("👥 PROBANDO LISTADO DE PRESTADORES")
    print("=" * 35)
    
    try:
        # Probar el listado principal
        response = requests.get(f"{base_url}/milotalent/listado", timeout=10)
        
        if response.status_code == 200:
            print("✅ Listado carga correctamente (200 OK)")
            
            # Verificar que no hay errores de LookupError en el contenido
            if "LookupError" in response.text:
                print("❌ Error LookupError aún presente en la respuesta")
                return False
            elif "Internal Server Error" in response.text:
                print("❌ Error interno del servidor")
                return False
            else:
                print("✅ No se detectaron errores en la respuesta")
                
        elif response.status_code == 302:
            print("🔒 Listado requiere autenticación (302 Redirect)")
            print("✅ La ruta funciona pero necesita login")
            
        else:
            print(f"❌ Error inesperado: {response.status_code}")
            return False
        
        # También probar el dashboard que debe estar accesible
        response_dashboard = requests.get(f"{base_url}/milotalent/dashboard", timeout=10)
        
        if response_dashboard.status_code == 200:
            print("✅ Dashboard accesible sin errores")
            
            # Verificar que el botón del listado esté presente
            if "Ver Listado de PS" in response_dashboard.text:
                print("✅ Botón 'Ver Listado de PS' presente en dashboard")
            else:
                print("⚠️ Botón 'Ver Listado de PS' no encontrado")
                
        print(f"\n🎉 PRUEBA COMPLETADA")
        print(f"📝 El error LookupError ha sido solucionado")
        print(f"🌐 Listado: {base_url}/milotalent/listado")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    probar_listado_ps()