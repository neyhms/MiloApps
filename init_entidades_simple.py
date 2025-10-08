#!/usr/bin/env python3
"""
Script simplificado para inicializar entidades usando el contexto existente
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Crear aplicación para contexto
from src.app import MiloAppsApp

def main():
    """Ejecutar inicialización"""
    print("🚀 INICIALIZANDO ENTIDADES TALENT")
    print("=" * 40)
    
    # Crear aplicación
    app_instance = MiloAppsApp()
    
    with app_instance.app.app_context():
        from src.models import db, TalentEntidad
        
        # Las tablas ya fueron creadas por MiloAppsApp
        print("✅ Contexto de aplicación establecido")
        
        # Crear datos de ejemplo básicos
        entidades_ejemplo = [
            # Municipios
            {'tipo_entidad': 'municipio', 'nombre': 'Bogotá D.C.', 'codigo': '11001', 'departamento': 'Bogotá D.C.'},
            {'tipo_entidad': 'municipio', 'nombre': 'Medellín', 'codigo': '05001', 'departamento': 'Antioquia'},
            {'tipo_entidad': 'municipio', 'nombre': 'Cali', 'codigo': '76001', 'departamento': 'Valle del Cauca'},
            
            # Profesiones
            {'tipo_entidad': 'profesion', 'nombre': 'Ingeniero de Sistemas', 'codigo': 'ING_SIS', 'orden': 1},
            {'tipo_entidad': 'profesion', 'nombre': 'Médico General', 'codigo': 'MED_GEN', 'orden': 2},
            {'tipo_entidad': 'profesion', 'nombre': 'Abogado', 'codigo': 'ABOGADO', 'orden': 3},
            {'tipo_entidad': 'profesion', 'nombre': 'Contador Público', 'codigo': 'CONT_PUB', 'orden': 4},
            {'tipo_entidad': 'profesion', 'nombre': 'Otros', 'codigo': 'OTROS', 'orden': 10, 'permite_otros': True},
            
            # Bancos
            {'tipo_entidad': 'banco', 'nombre': 'Bancolombia', 'codigo': '007', 'nit': '890903938-8', 'orden': 1},
            {'tipo_entidad': 'banco', 'nombre': 'Banco de Bogotá', 'codigo': '001', 'nit': '860002964-4', 'orden': 2},
            {'tipo_entidad': 'banco', 'nombre': 'BBVA Colombia', 'codigo': '013', 'nit': '860003020-1', 'orden': 3},
            {'tipo_entidad': 'banco', 'nombre': 'Davivienda', 'codigo': '051', 'nit': '860034313-7', 'orden': 4},
            {'tipo_entidad': 'banco', 'nombre': 'Otros', 'codigo': 'OTROS', 'orden': 10, 'permite_otros': True},
            
            # EPS
            {'tipo_entidad': 'eps', 'nombre': 'Sura EPS', 'codigo': 'EPS001', 'nit': '800088702-2', 'orden': 1},
            {'tipo_entidad': 'eps', 'nombre': 'Nueva EPS', 'codigo': 'EPS002', 'nit': '900156264-3', 'orden': 2},
            {'tipo_entidad': 'eps', 'nombre': 'Sanitas EPS', 'codigo': 'EPS003', 'nit': '800251440-6', 'orden': 3},
            {'tipo_entidad': 'eps', 'nombre': 'Salud Total EPS', 'codigo': 'EPS004', 'nit': '800130907-4', 'orden': 4},
            {'tipo_entidad': 'eps', 'nombre': 'Otros', 'codigo': 'OTROS', 'orden': 10, 'permite_otros': True},
            
            # AFP
            {'tipo_entidad': 'afp', 'nombre': 'Protección AFP', 'codigo': 'AFP001', 'nit': '800156998-0', 'orden': 1},
            {'tipo_entidad': 'afp', 'nombre': 'Porvenir AFP', 'codigo': 'AFP002', 'nit': '800144331-3', 'orden': 2},
            {'tipo_entidad': 'afp', 'nombre': 'Colfondos AFP', 'codigo': 'AFP003', 'nit': '800008578-7', 'orden': 3},
            {'tipo_entidad': 'afp', 'nombre': 'Colpensiones', 'codigo': 'COLP001', 'nit': '900336259-7', 'orden': 4},
            {'tipo_entidad': 'afp', 'nombre': 'Otros', 'codigo': 'OTROS', 'orden': 10, 'permite_otros': True},
            
            # ARL
            {'tipo_entidad': 'arl', 'nombre': 'Sura ARL', 'codigo': 'ARL001', 'nit': '800088702-2', 'orden': 1},
            {'tipo_entidad': 'arl', 'nombre': 'Positiva ARL', 'codigo': 'ARL002', 'nit': '800053635-1', 'orden': 2},
            {'tipo_entidad': 'arl', 'nombre': 'Colmena ARL', 'codigo': 'ARL003', 'nit': '860002180-3', 'orden': 3},
            {'tipo_entidad': 'arl', 'nombre': 'Liberty ARL', 'codigo': 'ARL004', 'nit': '860002183-8', 'orden': 4},
            {'tipo_entidad': 'arl', 'nombre': 'Otros', 'codigo': 'OTROS', 'orden': 10, 'permite_otros': True},
            
            # Caja de Compensación (opcional)
            {'tipo_entidad': 'caja_compensacion', 'nombre': 'Compensar', 'codigo': 'COMP001', 'nit': '860002503-1', 'orden': 1, 'es_obligatorio': False},
            {'tipo_entidad': 'caja_compensacion', 'nombre': 'Cafam', 'codigo': 'CAFAM001', 'nit': '860007387-5', 'orden': 2, 'es_obligatorio': False},
            {'tipo_entidad': 'caja_compensacion', 'nombre': 'Colsubsidio', 'codigo': 'COLS001', 'nit': '860007386-7', 'orden': 3, 'es_obligatorio': False},
            {'tipo_entidad': 'caja_compensacion', 'nombre': 'No Aplica', 'codigo': 'NA', 'orden': 8, 'es_obligatorio': False},
            {'tipo_entidad': 'caja_compensacion', 'nombre': 'Otros', 'codigo': 'OTROS', 'orden': 10, 'permite_otros': True, 'es_obligatorio': False},
            
            # Operador Seguridad Social
            {'tipo_entidad': 'operador_ss', 'nombre': 'Aportes en Línea', 'codigo': 'AEL001', 'nit': '900156264-3', 'orden': 1},
            {'tipo_entidad': 'operador_ss', 'nombre': 'Mi Planilla', 'codigo': 'MIP001', 'nit': '900337082-0', 'orden': 2},
            {'tipo_entidad': 'operador_ss', 'nombre': 'Simple', 'codigo': 'SIM001', 'nit': '900930737-0', 'orden': 3},
            {'tipo_entidad': 'operador_ss', 'nombre': 'SOI Planilla Integrada', 'codigo': 'SOI001', 'nit': '900156264-3', 'orden': 4},
            {'tipo_entidad': 'operador_ss', 'nombre': 'Otros', 'codigo': 'OTROS', 'orden': 10, 'permite_otros': True},
            
            # Área de Personal (pueden variar)
            {'tipo_entidad': 'area_personal', 'nombre': 'Recursos Humanos', 'codigo': 'RH001', 'orden': 1},
            {'tipo_entidad': 'area_personal', 'nombre': 'Talento Humano', 'codigo': 'TH001', 'orden': 2},
            {'tipo_entidad': 'area_personal', 'nombre': 'Gestión Humana', 'codigo': 'GH001', 'orden': 3},
            {'tipo_entidad': 'area_personal', 'nombre': 'Administración de Personal', 'codigo': 'AP001', 'orden': 4},
            {'tipo_entidad': 'area_personal', 'nombre': 'Nómina', 'codigo': 'NOM001', 'orden': 5},
            {'tipo_entidad': 'area_personal', 'nombre': 'Otros', 'codigo': 'OTROS', 'orden': 10, 'permite_otros': True},
        ]
        
        creadas = 0
        existentes = 0
        
        for datos in entidades_ejemplo:
            # Verificar si ya existe
            existe = TalentEntidad.query.filter_by(
                tipo_entidad=datos['tipo_entidad'],
                nombre=datos['nombre']
            ).first()
            
            if not existe:
                entidad = TalentEntidad(**datos)
                db.session.add(entidad)
                creadas += 1
            else:
                existentes += 1
        
        try:
            db.session.commit()
            print(f"✅ {creadas} entidades creadas, {existentes} ya existían")
            
            # Mostrar estadísticas
            tipos = ['municipio', 'profesion', 'banco', 'eps', 'afp', 'arl', 'caja_compensacion', 'operador_ss', 'area_personal']
            print("\n📊 ESTADÍSTICAS:")
            for tipo in tipos:
                count = TalentEntidad.query.filter_by(tipo_entidad=tipo, activo=True).count()
                print(f"   {tipo}: {count} registros")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()
        
        print("\n🎉 INICIALIZACIÓN COMPLETADA")

if __name__ == "__main__":
    main()