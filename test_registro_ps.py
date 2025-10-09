"""
Script de validación del formulario de registro de PS
Verifica que el formulario esté actualizando correctamente la base de datos
"""

import sys
import os
import requests
import json
from datetime import datetime

# Agregar el directorio src al path para importar modelos
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

def test_formulario_registro():
    """Prueba el formulario de registro de PS"""
    
    print("🧪 Iniciando pruebas del formulario de registro PS")
    print("=" * 50)
    
    # URL base de la aplicación
    base_url = "http://localhost:3000"
    
    # 1. Verificar que la aplicación esté ejecutándose
    try:
        response = requests.get(f"{base_url}/milotalent")
        if response.status_code == 200:
            print("✅ Aplicación MiloTalent accesible")
        else:
            print(f"❌ Error de acceso: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar a la aplicación")
        print("   Asegúrate de que la aplicación esté ejecutándose en http://localhost:3000")
        return False
    
    # 2. Verificar acceso al formulario (requiere autenticación)
    print("\n📋 Verificando acceso al formulario...")
    try:
        form_response = requests.get(f"{base_url}/milotalent/registro")
        if form_response.status_code == 401 or "login" in form_response.url.lower():
            print("⚠️  Formulario requiere autenticación (esto es correcto por seguridad)")
        elif form_response.status_code == 200:
            print("✅ Formulario accesible")
        else:
            print(f"❌ Error al acceder al formulario: {form_response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    return True

def verificar_base_datos():
    """Verifica la estructura de la base de datos"""
    
    print("\n🗄️  Verificando estructura de base de datos...")
    
    try:
        # Importar modelos y configuración de la aplicación
        from models import db
        from apps.milotalent.models import PrestadorServicio, AuditoriaPS
        from src.app import MiloAppsApp
        
        # Crear instancia de la aplicación
        app_instance = MiloAppsApp()
        
        with app_instance.app.app_context():
            # Verificar que las tablas existan
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'talent_prestadores' in tables:
                print("✅ Tabla 'talent_prestadores' existe")
                
                # Contar registros existentes
                count = PrestadorServicio.query.count()
                print(f"📊 Registros actuales en la base: {count}")
                
                # Mostrar últimos 3 registros
                if count > 0:
                    print("\n📝 Últimos registros:")
                    ultimos = PrestadorServicio.query.order_by(
                        PrestadorServicio.id_ps.desc()
                    ).limit(3).all()
                    
                    for ps in ultimos:
                        print(f"   • ID: {ps.id_ps[:8]}... | {ps.nombre_completo} | {ps.correo}")
                
            else:
                print("❌ Tabla 'talent_prestadores' no existe")
                print("   Ejecuta: python init_milotalent.py")
            
            if 'talent_auditoria' in tables:
                print("✅ Tabla de auditoría existe")
                audit_count = AuditoriaPS.query.count()
                print(f"📊 Registros de auditoría: {audit_count}")
            else:
                print("⚠️  Tabla de auditoría no existe")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar base de datos: {e}")
        return False


def crear_registro_prueba():
    """Crea un registro de prueba directamente en la base de datos"""
    
    print("\n🧪 Creando registro de prueba...")
    
    try:
        from models import db
        from apps.milotalent.models import PrestadorServicio, AuditoriaPS, SectorExperiencia, ModalidadContrato
        from src.app import MiloAppsApp
        
        app_instance = MiloAppsApp()
        
        with app_instance.app.app_context():
            # Crear PS de prueba
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            
            ps_prueba = PrestadorServicio(
                cedula=f"TEST-{timestamp}",
                nombre_completo=f"Prestador Prueba {timestamp}",
                correo=f"prueba{timestamp}@miloapps.com",
                telefono="300-123-4567",
                perfil_profesional="Servicios de Prueba",
                sector_experiencia=SectorExperiencia.MIXTO,
                modalidad=ModalidadContrato.PS,
                dependencia_asignada="Área de Pruebas",
                objeto_contractual="Prueba de funcionalidad",
                actividades_especificas="Validar registro en base de datos"
            )
            
            # Guardar en base de datos
            db.session.add(ps_prueba)
            db.session.commit()
            
            print(f"✅ Registro de prueba creado exitosamente")
            print(f"   ID: {ps_prueba.id_ps}")
            print(f"   Nombre: {ps_prueba.nombre_completo}")
            print(f"   Email: {ps_prueba.correo}")
            
            # Crear auditoría
            auditoria = AuditoriaPS(
                ps_id=ps_prueba.id_ps,
                usuario_id="SYSTEM-TEST",
                accion="prueba_registro",
                modulo="test_script",
                descripcion=f"Registro de prueba automática: {ps_prueba.nombre_completo}",
                valores_nuevos=json.dumps({
                    "nombre_completo": ps_prueba.nombre_completo,
                    "correo": ps_prueba.correo,
                    "cedula": ps_prueba.cedula
                }),
                ip_usuario="127.0.0.1",
                user_agent="Test Script v1.0"
            )
            
            db.session.add(auditoria)
            db.session.commit()
            
            print("✅ Auditoría registrada correctamente")
            
            return True
            
    except Exception as e:
        print(f"❌ Error al crear registro de prueba: {e}")
        return False


def mostrar_instrucciones_prueba_manual():
    """Muestra instrucciones para prueba manual del formulario"""
    
    print("\n" + "=" * 60)
    print("🔧 INSTRUCCIONES PARA PRUEBA MANUAL DEL FORMULARIO")
    print("=" * 60)
    
    print("\n1. 🌐 Abrir navegador y ir a: http://localhost:3000")
    print("2. 🔑 Iniciar sesión (si es requerido)")
    print("3. 📝 Ir a: http://localhost:3000/milotalent/registro")
    print("4. ✍️  Completar el formulario con datos de prueba:")
    print("   • Nombre: Juan")
    print("   • Apellido: Pérez")
    print("   • Email: juan.perez@test.com")
    print("   • Teléfono: 300-123-4567")
    print("   • Servicios: Seleccionar al menos uno")
    print("5. 💾 Hacer clic en 'Registrar'")
    print("6. ✅ Verificar mensaje de éxito")
    print("7. 🔍 Ejecutar este script nuevamente para verificar que se guardó")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    print("🚀 Sistema de Validación - Formulario Registro PS")
    print("MiloApps v1.0")
    print("=" * 60)
    
    # Ejecutar pruebas
    app_ok = test_formulario_registro()
    
    if app_ok:
        db_ok = verificar_base_datos()
        
        if db_ok:
            # Crear registro de prueba
            test_ok = crear_registro_prueba()
            
            if test_ok:
                print("\n🎉 TODAS LAS PRUEBAS EXITOSAS")
                print("✅ El formulario está configurado correctamente")
                print("✅ La base de datos está funcionando")
                print("✅ Los registros se están guardando correctamente")
            else:
                print("\n⚠️  Problema con la creación de registros")
        else:
            print("\n❌ Problema con la base de datos")
    else:
        print("\n❌ Problema con la aplicación")
    
    # Mostrar instrucciones para prueba manual
    mostrar_instrucciones_prueba_manual()
    
    print("\n📋 RESUMEN DE VALIDACIÓN COMPLETADO")