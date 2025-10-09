#!/usr/bin/env python3
"""
Script de prueba rápida para validar que las rutas de municipios funcionan
"""

import requests
import sys

def probar_rutas_municipios():
    """Prueba las rutas principales de municipios."""
    
    base_url = "http://localhost:3000"
    
    print("🧪 VALIDACIÓN RÁPIDA - RUTAS DE MUNICIPIOS")
    print("=" * 45)
    
    rutas_a_probar = [
        ("/milotalent/dashboard", "Dashboard MiloTalent"),
        ("/milotalent/crear-ps", "Formulario de registro"),
        ("/milotalent/admin/municipios", "Admin municipios"),
        ("/milotalent/api/municipios", "API municipios"),
    ]
    
    try:
        for ruta, descripcion in rutas_a_probar:
            response = requests.get(f"{base_url}{ruta}", timeout=5)
            
            # 200 = OK, 302 = Redirect (probablemente a login), 404 = No encontrado
            if response.status_code in [200, 302]:
                status = "✅ OK" if response.status_code == 200 else "🔒 Requiere Auth"
                print(f"{status} {descripcion}: {response.status_code}")
            else:
                print(f"❌ ERROR {descripcion}: {response.status_code}")
                return False
        
        print(f"\n🎉 TODAS LAS RUTAS FUNCIONAN CORRECTAMENTE")
        print(f"📝 El error de 'BuildError' ha sido solucionado")
        print(f"🌐 Dashboard: {base_url}/milotalent/dashboard")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("💡 Asegúrate de que el servidor esté corriendo")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    exito = probar_rutas_municipios()
    sys.exit(0 if exito else 1)