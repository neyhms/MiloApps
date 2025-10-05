# Test de la nueva estructura modular de MiloApps
import sys
import os

# Agregar src al path para importar módulos
sys.path.insert(0, 'src')

def test_imports():
    """Probar que todos los imports funcionen correctamente"""
    print("🧪 PROBANDO NUEVA ESTRUCTURA MODULAR...")
    print("=" * 50)
    
    try:
        # Probar imports del core
        print("📦 Probando imports del core...")
        from core.models import User, db, create_initial_data
        print("   ✅ Models importado correctamente")
        
        from core.config import get_config
        print("   ✅ Config importado correctamente")
        
        from core.utils import log_audit, get_user_apps
        print("   ✅ Utils importado correctamente")
        
        print("✅ CORE: Todos los imports funcionan")
        print()
        
        # Probar imports de la app de auth
        print("🔐 Probando imports de Auth App...")
        try:
            from apps.auth.routes import auth_bp
            print("   ✅ Auth routes importado correctamente")
        except ImportError as e:
            print(f"   ⚠️ Error en auth routes: {e}")
        
        try:
            from apps.auth.forms import LoginForm
            print("   ✅ Auth forms importado correctamente")
        except ImportError as e:
            print(f"   ⚠️ Error en auth forms: {e}")
        
        print("✅ AUTH APP: Estructura lista")
        print()
        
        # Probar imports de MiloSign
        print("✍️ Probando imports de MiloSign App...")
        try:
            from apps.milosign.routes import milosign_bp
            print("   ✅ MiloSign routes importado correctamente")
        except ImportError as e:
            print(f"   ⚠️ Error en milosign routes: {e}")
        
        try:
            from apps.milosign.models import Document
            print("   ✅ MiloSign models importado correctamente")
        except ImportError as e:
            print(f"   ⚠️ Error en milosign models: {e}")
        
        print("✅ MILOSIGN APP: Estructura lista")
        print()
        
        # Probar la aplicación principal
        print("🚀 Probando aplicación principal...")
        from app_new import create_app
        print("   ✅ App factory importado correctamente")
        
        # Crear instancia de prueba
        app = create_app('testing')
        print("   ✅ Aplicación creada correctamente")
        
        print("✅ APLICACIÓN PRINCIPAL: Lista para usar")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_structure():
    """Verificar que la estructura de archivos esté correcta"""
    print("📁 VERIFICANDO ESTRUCTURA DE ARCHIVOS...")
    print("=" * 50)
    
    expected_files = [
        'src/core/__init__.py',
        'src/core/models.py',
        'src/core/config.py', 
        'src/core/utils.py',
        'src/apps/auth/routes.py',
        'src/apps/auth/forms.py',
        'src/apps/milosign/routes.py',
        'src/apps/milosign/models.py',
        'src/apps/milosign/forms.py',
        'src/app_new.py'
    ]
    
    missing_files = []
    
    for file_path in expected_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - FALTANTE")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ ARCHIVOS FALTANTES: {len(missing_files)}")
        return False
    else:
        print("\n✅ ESTRUCTURA COMPLETA")
        return True

def main():
    """Función principal de prueba"""
    print("🎯 INICIANDO PRUEBAS DE ESTRUCTURA MODULAR")
    print("=" * 60)
    print()
    
    # Cambiar al directorio raíz del proyecto
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Probar estructura de archivos
    structure_ok = test_structure()
    print()
    
    # Probar imports si la estructura está bien
    if structure_ok:
        imports_ok = test_imports()
        print()
        
        if imports_ok:
            print("🎉 ¡ESTRUCTURA MODULAR LISTA!")
            print("=" * 60)
            print()
            print("📋 PRÓXIMOS PASOS:")
            print("1. Detener el servidor actual")
            print("2. Reemplazar app.py por app_new.py")
            print("3. Actualizar templates para usar nueva estructura")
            print("4. Probar cada aplicación individualmente")
            print("5. Migrar datos si es necesario")
            print()
            print("🚀 PARA INICIAR CON NUEVA ESTRUCTURA:")
            print("   python src/app_new.py")
        else:
            print("❌ HAY ERRORES EN LOS IMPORTS")
            print("🔧 Revisa los errores y corrígelos antes de continuar")
    else:
        print("❌ LA ESTRUCTURA NO ESTÁ COMPLETA")
        print("🔧 Crea los archivos faltantes primero")

if __name__ == '__main__':
    main()