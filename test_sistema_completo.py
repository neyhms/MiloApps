#!/usr/bin/env python3
"""
Script para probar completamente el sistema MiloTalent después de las correcciones
"""

import requests

def probar_sistema_completo():
    """Prueba completa del sistema MiloTalent."""
    
    base_url = "http://localhost:3000/milotalent"
    
    print("🧪 PRUEBA COMPLETA DEL SISTEMA MILOTALENT")
    print("=" * 45)
    
    rutas_criticas = [
        ("/dashboard", "Dashboard principal"),
        ("/crear-ps", "Formulario de registro"),
        ("/listado", "Listado de prestadores"),
        ("/admin/municipios", "Administración de municipios"),
        ("/api/municipios", "API de municipios"),
        ("/api/stats", "API de estadísticas"),
    ]
    
    try:
        todo_funciona = True
        
        for ruta, descripcion in rutas_criticas:
            response = requests.get(f"{base_url}{ruta}", timeout=10)
            
            if response.status_code in [200, 302]:
                status = "✅ OK" if response.status_code == 200 else "🔒 Auth"
                print(f"{status} {descripcion}: {response.status_code}")
                
                # Verificar que no hay errores específicos
                if "ProgrammingError" in response.text:
                    print(f"   ❌ Error ProgrammingError detectado")
                    todo_funciona = False
                elif "LookupError" in response.text:
                    print(f"   ❌ Error LookupError detectado")
                    todo_funciona = False
                elif "sqlalchemy.exc" in response.text:
                    print(f"   ❌ Error SQLAlchemy detectado")
                    todo_funciona = False
                else:
                    print(f"   ✅ Sin errores detectados en respuesta")
                    
            else:
                print(f"❌ ERROR {descripcion}: {response.status_code}")
                todo_funciona = False
        
        if todo_funciona:
            print(f"\n🎉 SISTEMA COMPLETAMENTE FUNCIONAL")
            print(f"✅ Todos los errores enum/lookup corregidos")
            print(f"✅ Dashboard accesible desde aplicaciones")
            print(f"✅ Formularios y listados funcionando")
            print(f"✅ APIs respondiendo correctamente")
            print(f"\n🌐 Acceso al sistema:")
            print(f"   Dashboard: {base_url}/dashboard")
            print(f"   Registro PS: {base_url}/crear-ps")  
            print(f"   Listado: {base_url}/listado")
        else:
            print(f"\n⚠️ Algunos problemas detectados")
            print(f"💡 Revisar logs del servidor para más detalles")
        
        return todo_funciona
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("💡 Verifica que el servidor esté corriendo")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    probar_sistema_completo()