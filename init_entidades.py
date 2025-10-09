#!/usr/bin/env python3
"""
Script para inicializar el sistema de entidades genéricas de Talent
Carga datos por defecto para todas las entidades administrativas
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.models import db, TalentEntidad, crear_entidad_inicial
from src.app import MiloAppsApp

# Datos iniciales por tipo de entidad
DATOS_INICIALES = {
    'municipio': [
        {'nombre': 'Bogotá D.C.', 'codigo': '11001', 'departamento': 'Bogotá D.C.', 'codigo_dane': '11001'},
        {'nombre': 'Medellín', 'codigo': '05001', 'departamento': 'Antioquia', 'codigo_dane': '05001'},
        {'nombre': 'Cali', 'codigo': '76001', 'departamento': 'Valle del Cauca', 'codigo_dane': '76001'},
        {'nombre': 'Barranquilla', 'codigo': '08001', 'departamento': 'Atlántico', 'codigo_dane': '08001'},
        {'nombre': 'Cartagena', 'codigo': '13001', 'departamento': 'Bolívar', 'codigo_dane': '13001'},
        {'nombre': 'Bucaramanga', 'codigo': '68001', 'departamento': 'Santander', 'codigo_dane': '68001'},
        {'nombre': 'Pereira', 'codigo': '66001', 'departamento': 'Risaralda', 'codigo_dane': '66001'},
        {'nombre': 'Manizales', 'codigo': '17001', 'departamento': 'Caldas', 'codigo_dane': '17001'},
        {'nombre': 'Santa Marta', 'codigo': '47001', 'departamento': 'Magdalena', 'codigo_dane': '47001'},
        {'nombre': 'Cúcuta', 'codigo': '54001', 'departamento': 'Norte de Santander', 'codigo_dane': '54001'},
    ],
    
    'profesion': [
        {'nombre': 'Ingeniero de Sistemas', 'codigo': 'ING_SIS', 'orden': 1},
        {'nombre': 'Médico General', 'codigo': 'MED_GEN', 'orden': 2},
        {'nombre': 'Abogado', 'codigo': 'ABOGADO', 'orden': 3},
        {'nombre': 'Contador Público', 'codigo': 'CONT_PUB', 'orden': 4},
        {'nombre': 'Administrador de Empresas', 'codigo': 'ADM_EMP', 'orden': 5},
        {'nombre': 'Psicólogo', 'codigo': 'PSICOLOGO', 'orden': 6},
        {'nombre': 'Enfermero', 'codigo': 'ENFERMERO', 'orden': 7},
        {'nombre': 'Arquitecto', 'codigo': 'ARQUITECTO', 'orden': 8},
        {'nombre': 'Diseñador Gráfico', 'codigo': 'DIS_GRAF', 'orden': 9},
        {'nombre': 'Técnico', 'codigo': 'TECNICO', 'orden': 10},
        {'nombre': 'Tecnólogo', 'codigo': 'TECNOLOGO', 'orden': 11},
        {'nombre': 'Otros', 'codigo': 'OTROS', 'orden': 12, 'permite_otros': True},
    ],
    
    'banco': [
        {'nombre': 'Bancolombia', 'codigo': '007', 'nit': '890903938-8', 'orden': 1},
        {'nombre': 'Banco de Bogotá', 'codigo': '001', 'nit': '860002964-4', 'orden': 2},
        {'nombre': 'Banco Popular', 'codigo': '002', 'nit': '860007738-9', 'orden': 3},
        {'nombre': 'BBVA Colombia', 'codigo': '013', 'nit': '860003020-1', 'orden': 4},
        {'nombre': 'Banco Davivienda', 'codigo': '051', 'nit': '860034313-7', 'orden': 5},
        {'nombre': 'Banco de Occidente', 'codigo': '023', 'nit': '890903937-1', 'orden': 6},
        {'nombre': 'Banco Caja Social', 'codigo': '032', 'nit': '860007335-9', 'orden': 7},
        {'nombre': 'Banco AV Villas', 'codigo': '052', 'nit': '860035827-6', 'orden': 8},
        {'nombre': 'Citibank', 'codigo': '009', 'nit': '860034594-6', 'orden': 9},
        {'nombre': 'Banco Agrario', 'codigo': '040', 'nit': '800037800-8', 'orden': 10},
        {'nombre': 'Nequi', 'codigo': 'NEQ', 'nit': '890903938-8', 'orden': 11},
        {'nombre': 'Daviplata', 'codigo': 'DAV', 'nit': '860034313-7', 'orden': 12},
        {'nombre': 'Otros', 'codigo': 'OTROS', 'orden': 13, 'permite_otros': True},
    ],
    
    'eps': [
        {'nombre': 'Sura EPS', 'codigo': 'EPS001', 'nit': '800088702-2', 'orden': 1},
        {'nombre': 'Nueva EPS', 'codigo': 'EPS002', 'nit': '900156264-3', 'orden': 2},
        {'nombre': 'Sanitas EPS', 'codigo': 'EPS003', 'nit': '800251440-6', 'orden': 3},
        {'nombre': 'Salud Total EPS', 'codigo': 'EPS004', 'nit': '800130907-4', 'orden': 4},
        {'nombre': 'Compensar EPS', 'codigo': 'EPS005', 'nit': '860002503-1', 'orden': 5},
        {'nombre': 'Famisanar EPS', 'codigo': 'EPS006', 'nit': '800037826-6', 'orden': 6},
        {'nombre': 'Cafesalud EPS', 'codigo': 'EPS007', 'nit': '900047981-5', 'orden': 7},
        {'nombre': 'Coomeva EPS', 'codigo': 'EPS008', 'nit': '890300279-2', 'orden': 8},
        {'nombre': 'Medimás EPS', 'codigo': 'EPS009', 'nit': '901103047-9', 'orden': 9},
        {'nombre': 'Capital Salud EPS', 'codigo': 'EPS010', 'nit': '900298372-4', 'orden': 10},
        {'nombre': 'Otros', 'codigo': 'OTROS', 'orden': 11, 'permite_otros': True},
    ],
    
    'afp': [
        {'nombre': 'Protección AFP', 'codigo': 'AFP001', 'nit': '800156998-0', 'orden': 1},
        {'nombre': 'Porvenir AFP', 'codigo': 'AFP002', 'nit': '800144331-3', 'orden': 2},
        {'nombre': 'Colfondos AFP', 'codigo': 'AFP003', 'nit': '800008578-7', 'orden': 3},
        {'nombre': 'Old Mutual AFP', 'codigo': 'AFP004', 'nit': '800156804-7', 'orden': 4},
        {'nombre': 'Colpensiones', 'codigo': 'COLP001', 'nit': '900336259-7', 'orden': 5},
        {'nombre': 'Otros', 'codigo': 'OTROS', 'orden': 6, 'permite_otros': True},
    ],
    
    'arl': [
        {'nombre': 'Sura ARL', 'codigo': 'ARL001', 'nit': '800088702-2', 'orden': 1},
        {'nombre': 'Positiva ARL', 'codigo': 'ARL002', 'nit': '800053635-1', 'orden': 2},
        {'nombre': 'Colmena ARL', 'codigo': 'ARL003', 'nit': '860002180-3', 'orden': 3},
        {'nombre': 'Liberty ARL', 'codigo': 'ARL004', 'nit': '860002183-8', 'orden': 4},
        {'nombre': 'Equidad ARL', 'codigo': 'ARL005', 'nit': '860026726-1', 'orden': 5},
        {'nombre': 'Bolivar ARL', 'codigo': 'ARL006', 'nit': '860002503-1', 'orden': 6},
        {'nombre': 'Otros', 'codigo': 'OTROS', 'orden': 7, 'permite_otros': True},
    ],
    
    'caja_compensacion': [
        {'nombre': 'Compensar', 'codigo': 'COMP001', 'nit': '860002503-1', 'orden': 1, 'es_obligatorio': False},
        {'nombre': 'Cafam', 'codigo': 'CAFAM001', 'nit': '860007387-5', 'orden': 2, 'es_obligatorio': False},
        {'nombre': 'Colsubsidio', 'codigo': 'COLS001', 'nit': '860007386-7', 'orden': 3, 'es_obligatorio': False},
        {'nombre': 'Comfama', 'codigo': 'COMF001', 'nit': '890900341-5', 'orden': 4, 'es_obligatorio': False},
        {'nombre': 'Comfenalco Antioquia', 'codigo': 'COMFA001', 'nit': '890900539-6', 'orden': 5, 'es_obligatorio': False},
        {'nombre': 'Comfandi', 'codigo': 'COMFD001', 'nit': '890399032-5', 'orden': 6, 'es_obligatorio': False},
        {'nombre': 'Comfacauca', 'codigo': 'COMFC001', 'nit': '891500356-1', 'orden': 7, 'es_obligatorio': False},
        {'nombre': 'No Aplica', 'codigo': 'NA', 'orden': 8, 'es_obligatorio': False},
        {'nombre': 'Otros', 'codigo': 'OTROS', 'orden': 9, 'permite_otros': True, 'es_obligatorio': False},
    ],
    
    'operador_ss': [
        {'nombre': 'Aportes en Línea', 'codigo': 'AEL001', 'nit': '900156264-3', 'orden': 1},
        {'nombre': 'Mi Planilla', 'codigo': 'MIP001', 'nit': '900337082-0', 'orden': 2},
        {'nombre': 'Simple', 'codigo': 'SIM001', 'nit': '900930737-0', 'orden': 3},
        {'nombre': 'SOI Planilla Integrada', 'codigo': 'SOI001', 'nit': '900156264-3', 'orden': 4},
        {'nombre': 'Planilla Net', 'codigo': 'PN001', 'nit': '830002964-4', 'orden': 5},
        {'nombre': 'Emssanar', 'codigo': 'EMS001', 'nit': '900298372-4', 'orden': 6},
        {'nombre': 'Otros', 'codigo': 'OTROS', 'orden': 7, 'permite_otros': True},
    ],
    
    'area_personal': [
        {'nombre': 'Recursos Humanos', 'codigo': 'RH001', 'orden': 1},
        {'nombre': 'Talento Humano', 'codigo': 'TH001', 'orden': 2},
        {'nombre': 'Gestión Humana', 'codigo': 'GH001', 'orden': 3},
        {'nombre': 'Administración de Personal', 'codigo': 'AP001', 'orden': 4},
        {'nombre': 'Nómina', 'codigo': 'NOM001', 'orden': 5},
        {'nombre': 'Contratación', 'codigo': 'CONT001', 'orden': 6},
        {'nombre': 'Selección', 'codigo': 'SEL001', 'orden': 7},
        {'nombre': 'Bienestar', 'codigo': 'BIEN001', 'orden': 8},
        {'nombre': 'Capacitación', 'codigo': 'CAP001', 'orden': 9},
        {'nombre': 'Desarrollo Organizacional', 'codigo': 'DO001', 'orden': 10},
        {'nombre': 'Otros', 'codigo': 'OTROS', 'orden': 11, 'permite_otros': True},
    ]
}

def inicializar_entidades():
    """Inicializa todas las entidades del sistema"""
    
    app_instance = MiloAppsApp()
    app = app_instance.app
    
    with app.app_context():
        print("🚀 INICIALIZANDO SISTEMA DE ENTIDADES TALENT")
        print("=" * 50)
        
        # Crear tablas
        db.create_all()
        print("✅ Tablas de base de datos creadas")
        
        total_creadas = 0
        total_existentes = 0
        
        # Procesar cada tipo de entidad
        for tipo_entidad, entidades in DATOS_INICIALES.items():
            print(f"\n📂 Procesando {tipo_entidad.upper()}...")
            
            creadas = 0
            existentes = 0
            
            for datos in entidades:
                entidad = crear_entidad_inicial(tipo_entidad, **datos)
                
                if entidad.id:  # Ya existe
                    existentes += 1
                else:  # Se creó nueva
                    creadas += 1
            
            try:
                db.session.commit()
                print(f"   ✅ {creadas} nuevas, {existentes} existentes")
            except Exception as e:
                print(f"   ❌ Error: {e}")
                db.session.rollback()
                continue
            
            total_creadas += creadas
            total_existentes += existentes
        
        print(f"\n🎉 INICIALIZACIÓN COMPLETADA")
        print(f"   📊 {total_creadas} entidades creadas")
        print(f"   📊 {total_existentes} entidades ya existían")
        print(f"   📊 Total: {total_creadas + total_existentes} entidades")
        
        # Mostrar estadísticas por tipo
        print(f"\n📈 ESTADÍSTICAS POR TIPO:")
        for tipo in DATOS_INICIALES.keys():
            count = TalentEntidad.query.filter_by(tipo_entidad=tipo, activo=True).count()
            print(f"   {tipo}: {count} activas")
        
        return True

if __name__ == "__main__":
    inicializar_entidades()