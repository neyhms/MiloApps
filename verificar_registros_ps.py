"""
Script para verificar directamente la base de datos de MiloTalent
Verifica que los registros del formulario se estén guardando correctamente
"""

import sys
import os
from datetime import datetime
import json

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

def verificar_registros_ps():
    """Verifica los registros existentes en la base de datos"""
    
    print("🔍 VERIFICACIÓN DE BASE DE DATOS - REGISTROS PS")
    print("=" * 60)
    
    try:
        # Importar modelos y configuración
        from models import db
        from apps.milotalent.models import PrestadorServicio, AuditoriaPS
        from src.app import MiloAppsApp
        
        # Crear instancia de la aplicación
        app_instance = MiloAppsApp()
        
        with app_instance.app.app_context():
            # Verificar conectividad a BD
            try:
                db.engine.execute("SELECT 1")
                print("✅ Conexión a base de datos exitosa")
            except Exception as e:
                print(f"❌ Error de conexión a BD: {e}")
                return False
            
            # Contar total de registros
            total_ps = PrestadorServicio.query.count()
            print(f"📊 Total de Prestadores registrados: {total_ps}")
            
            if total_ps == 0:
                print("⚠️  No hay registros en la base de datos")
                print("   Esto puede indicar que:")
                print("   • El formulario no está guardando correctamente")
                print("   • No se han hecho registros aún")
                print("   • Hay un problema con la BD")
                return False
            
            # Mostrar últimos 5 registros
            print(f"\n📝 Últimos {min(5, total_ps)} registros:")
            ultimos = PrestadorServicio.query.order_by(
                PrestadorServicio.id_ps.desc()
            ).limit(5).all()
            
            for i, ps in enumerate(ultimos, 1):
                print(f"\n   {i}. ID: {ps.id_ps[:8]}...")
                print(f"      Nombre: {ps.nombre_completo}")
                print(f"      Email: {ps.correo}")
                print(f"      Teléfono: {ps.telefono}")
                print(f"      Servicios: {ps.perfil_profesional}")
                print(f"      Dependencia: {ps.dependencia_asignada}")
            
            # Verificar auditoría
            total_audit = AuditoriaPS.query.count()
            print(f"\n📋 Registros de auditoría: {total_audit}")
            
            if total_audit > 0:
                print("\n🔍 Últimas 3 acciones de auditoría:")
                auditorias = AuditoriaPS.query.order_by(
                    AuditoriaPS.fecha_hora.desc()
                ).limit(3).all()
                
                for i, audit in enumerate(auditorias, 1):
                    print(f"   {i}. Acción: {audit.accion}")
                    print(f"      Módulo: {audit.modulo}")
                    print(f"      Usuario: {audit.usuario_id}")
                    print(f"      Fecha: {audit.fecha_hora}")
                    print(f"      Descripción: {audit.descripcion}")
                    print()
            
            return True
            
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("   Verifica que los módulos estén correctamente instalados")
        return False
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

def probar_insercion_directa():
    """Prueba insertar un registro directamente para verificar funcionalidad"""
    
    print("\n🧪 PRUEBA DE INSERCIÓN DIRECTA")
    print("=" * 40)
    
    try:
        from models import db
        from apps.milotalent.models import (
            PrestadorServicio, 
            AuditoriaPS, 
            SectorExperiencia, 
            ModalidadContrato
        )
        from src.app import MiloAppsApp
        
        app_instance = MiloAppsApp()
        
        with app_instance.app.app_context():
            # Crear registro de prueba
            timestamp = datetime.now().strftime('%m%d_%H%M%S')
            
            ps_test = PrestadorServicio(
                cedula=f"12345{timestamp}",
                nombre_completo=f"Prueba Formulario {timestamp}",
                correo=f"test{timestamp}@miloapps.com",
                telefono="300-555-0123",
                perfil_profesional="Electricidad, Plomería",
                sector_experiencia=SectorExperiencia.MIXTO,
                modalidad=ModalidadContrato.PS,
                dependencia_asignada="Departamento de Pruebas",
                objeto_contractual="Validación de formulario de registro",
                actividades_especificas="Servicios de: Electricidad, Plomería"
            )
            
            # Intentar guardar
            db.session.add(ps_test)
            db.session.commit()
            
            print("✅ Registro de prueba insertado exitosamente")
            print(f"   ID generado: {ps_test.id_ps}")
            print(f"   Nombre: {ps_test.nombre_completo}")
            
            # Crear auditoría correspondiente
            audit_test = AuditoriaPS(
                ps_id=ps_test.id_ps,
                usuario_id="SCRIPT_TEST",
                accion="insercion_prueba",
                modulo="verificacion_bd",
                descripcion=f"Prueba de inserción directa: {ps_test.nombre_completo}",
                valores_nuevos=json.dumps({
                    "nombre_completo": ps_test.nombre_completo,
                    "correo": ps_test.correo,
                    "cedula": ps_test.cedula,
                    "telefono": ps_test.telefono
                }),
                ip_usuario="127.0.0.1",
                user_agent="Verification Script"
            )
            
            db.session.add(audit_test)
            db.session.commit()
            
            print("✅ Auditoría registrada correctamente")
            
            return True
            
    except Exception as e:
        print(f"❌ Error en inserción directa: {e}")
        db.session.rollback()  # Rollback en caso de error
        return False

def buscar_registros_recientes():
    """Busca registros que puedan haber sido creados por el formulario web"""
    
    print("\n🔍 BÚSQUEDA DE REGISTROS RECIENTES")
    print("=" * 40)
    
    try:
        from models import db
        from apps.milotalent.models import PrestadorServicio, AuditoriaPS
        from src.app import MiloAppsApp
        from datetime import datetime, timedelta
        
        app_instance = MiloAppsApp()
        
        with app_instance.app.app_context():
            # Buscar registros de las últimas 24 horas
            hace_24h = datetime.now() - timedelta(hours=24)
            
            # Como no tenemos fecha_creacion, busquemos por auditoría
            auditorias_recientes = AuditoriaPS.query.filter(
                AuditoriaPS.fecha_hora >= hace_24h,
                AuditoriaPS.accion == "registro"
            ).order_by(AuditoriaPS.fecha_hora.desc()).all()
            
            if auditorias_recientes:
                print(f"📅 Encontrados {len(auditorias_recientes)} registros recientes:")
                
                for audit in auditorias_recientes:
                    # Buscar el PS correspondiente
                    ps = PrestadorServicio.query.filter_by(id_ps=audit.ps_id).first()
                    if ps:
                        print(f"\n   🆔 ID: {ps.id_ps[:8]}...")
                        print(f"   👤 Nombre: {ps.nombre_completo}")
                        print(f"   📧 Email: {ps.correo}")
                        print(f"   📱 Teléfono: {ps.telefono}")
                        print(f"   🔧 Servicios: {ps.perfil_profesional}")
                        print(f"   ⏰ Registrado: {audit.fecha_hora}")
                        print(f"   👨‍💻 Usuario: {audit.usuario_id}")
                        
                        # Verificar si fue desde formulario web
                        if audit.ip_usuario and audit.user_agent:
                            print(f"   🌐 IP: {audit.ip_usuario}")
                            if "Mozilla" in audit.user_agent:
                                print("   ✅ Registrado desde navegador web (formulario)")
                            else:
                                print("   🤖 Registrado desde script/API")
            else:
                print("📭 No se encontraron registros recientes de las últimas 24 horas")
                print("   Esto podría indicar que:")
                print("   • El formulario web no está funcionando")
                print("   • No se han hecho registros recientemente")
                print("   • Hay un problema con la auditoría")
            
            return True
            
    except Exception as e:
        print(f"❌ Error en búsqueda de registros recientes: {e}")
        return False

if __name__ == "__main__":
    print("🏥 DIAGNÓSTICO DE BASE DE DATOS - MILOTALENT")
    print("Verificación de formulario de registro PS")
    print("=" * 60)
    
    # 1. Verificar registros existentes
    exito_verificacion = verificar_registros_ps()
    
    # 2. Buscar registros recientes (formulario web)
    buscar_registros_recientes()
    
    # 3. Probar inserción directa
    exito_insercion = probar_insercion_directa()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📋 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 60)
    
    if exito_verificacion and exito_insercion:
        print("✅ La base de datos está funcionando correctamente")
        print("✅ Las inserciones se procesan sin problemas")
        print("✅ El modelo de datos está bien configurado")
        print("\n💡 Si el formulario web no funciona, el problema puede ser:")
        print("   • Errores en la validación del formulario")
        print("   • Problemas con CSRF tokens")
        print("   • Errores de autenticación")
        print("   • Errores en la lógica de la ruta /procesar")
    else:
        print("❌ Hay problemas con la base de datos")
        print("🔧 Recomendaciones:")
        print("   • Verificar que las tablas estén creadas")
        print("   • Ejecutar: python init_milotalent.py")
        print("   • Revisar permisos de la base de datos")
        print("   • Verificar configuración de SQLAlchemy")
    
    print("\n🎯 Para probar el formulario manualmente, ve a:")
    print("   http://localhost:3000/milotalent/registro")