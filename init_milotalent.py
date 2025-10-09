"""
Script para recrear la base de datos con la nueva estructura
"""

import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

def recrear_base_datos():
    """Recrear base de datos con nueva estructura"""
    
    print("🗄️  RECREANDO BASE DE DATOS - NUEVA ESTRUCTURA PS")
    print("=" * 60)
    
    try:
        from models import db
        from apps.milotalent.models import PrestadorServicio, AuditoriaPS
        from src.app import MiloAppsApp
        
        # Crear instancia de la aplicación
        app_instance = MiloAppsApp()
        
        with app_instance.app.app_context():
            print("🔄 Eliminando tablas existentes...")
            
            # Eliminar todas las tablas relacionadas con milotalent
            from sqlalchemy import text
            db.session.execute(text("DROP TABLE IF EXISTS talent_auditoria"))
            db.session.execute(text("DROP TABLE IF EXISTS talent_prestadores"))  
            db.session.execute(text("DROP TABLE IF EXISTS talent_cdp"))
            db.session.execute(text("DROP TABLE IF EXISTS talent_expedientes"))
            db.session.execute(text("DROP TABLE IF EXISTS talent_documentos"))
            db.session.execute(text("DROP TABLE IF EXISTS talent_contratos"))
            db.session.execute(text("DROP TABLE IF EXISTS talent_alertas"))
            
            db.session.commit()
            print("✅ Tablas antiguas eliminadas")
            
            print("🔨 Creando nuevas tablas...")
            
            # Crear las nuevas tablas
            db.create_all()
            
            print("✅ Nuevas tablas creadas exitosamente")
            
            # Verificar que las tablas se crearon
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"\n📋 Tablas en la base de datos:")
            for table in tables:
                if 'talent' in table:
                    print(f"   ✅ {table}")
            
            print(f"\n🎉 Base de datos recreada exitosamente")
            print(f"📊 Registros en talent_prestadores_new: {PrestadorServicio.query.count()}")
            
    except Exception as e:
        print(f"❌ Error recreando base de datos: {e}")
        import traceback
        traceback.print_exc()


def init_milotalent_tables():
    """Mantener compatibilidad con nombre anterior"""
    return recrear_base_datos()
    print("🗄️  Inicializando tablas de MiloTalent...")

    try:
        # Crear tablas
        db.create_all()
        print("✅ Tablas de MiloTalent creadas exitosamente")

        return True

    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        return False


if __name__ == "__main__":
    # Configurar Flask app para el contexto de base de datos
    from src.app import MiloAppsApp

    app_instance = MiloAppsApp()

    with app_instance.app.app_context():
        success = init_milotalent_tables()

        if success:
            print("\n🎉 MiloTalent inicializado correctamente")
            print("📋 Tablas creadas:")
            print("   - talent_prestadores (Prestadores de Servicios)")
            print("   - talent_cdp (Certificados de Disponibilidad Presupuestal)")
            print("   - talent_expedientes (Expedientes Precontractuales)")
            print("   - talent_historial_contratos (Historial de Contratos)")
            print("   - talent_documentos (Documentos de PS)")
            print("   - talent_alertas (Sistema de Alertas)")
            print("   - talent_auditoria (Auditoría y Trazabilidad)")
        else:
            print("\n❌ Error en la inicialización")
            sys.exit(1)
