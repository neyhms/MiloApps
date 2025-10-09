"""
Script simple para verificar los registros PS en la base de datos
"""

import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

def main():
    print("🔍 VERIFICACIÓN SIMPLE DE REGISTROS PS")
    print("=" * 50)
    
    try:
        from models import db
        from apps.milotalent.models import PrestadorServicio
        from src.app import MiloAppsApp
        
        app_instance = MiloAppsApp()
        
        with app_instance.app.app_context():
            # Contar todos los registros
            total = PrestadorServicio.query.count()
            print(f"📊 Total de Prestadores: {total}")
            
            if total > 0:
                print(f"\n📋 Lista de todos los PS registrados:")
                prestadores = PrestadorServicio.query.all()
                
                for i, ps in enumerate(prestadores, 1):
                    print(f"\n{i}. {ps.nombre_completo}")
                    print(f"   📧 {ps.correo}")
                    print(f"   📱 {ps.telefono}")
                    print(f"   🆔 {ps.cedula}")
                    print(f"   🔧 {ps.perfil_profesional}")
                
                # Verificar si hay registros que podrían ser del formulario web
                registros_temp = [ps for ps in prestadores if ps.cedula.startswith('TEMP-')]
                if registros_temp:
                    print(f"\n✅ {len(registros_temp)} registros temporales encontrados")
                    print("   (Estos probablemente vienen del formulario web)")
                    
                    for ps in registros_temp[-3:]:  # Últimos 3
                        print(f"   • {ps.nombre_completo} - {ps.correo}")
                
            else:
                print("📭 No hay registros en la base de datos")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()