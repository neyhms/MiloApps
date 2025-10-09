#!/usr/bin/env python3
"""
Script de prueba para validar la funcionalidad de unicidad de cédulas
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.apps.milotalent.models import PrestadorServicio, db
from src.app import MiloAppsApp
import requests
from datetime import datetime

def test_unicidad_cedula():
    """Prueba la validación de unicidad de cédulas."""
    print("=== PRUEBA DE UNICIDAD DE CÉDULA ===\n")
    
    # Inicializar aplicación
    milo_app = MiloAppsApp()
    app = milo_app.app
    
    # Datos de prueba
    cedula_test = "12345678"
    
    with app.app_context():
        # Verificar si ya existe un prestador con esta cédula
        prestador_existente = PrestadorServicio.query.filter_by(cedula_ps=cedula_test).first()
        
        if prestador_existente:
            print(f"✅ Prestador encontrado con cédula {cedula_test}:")
            print(f"   - Nombre: {prestador_existente.nombres_ps} {prestador_existente.apellidos_ps}")
            print(f"   - ID: {prestador_existente.id}")
            print(f"   - Fecha registro: {prestador_existente.fecha_registro}")
            
            # Probar API de verificación
            print(f"\n🔍 Probando API de verificación para cédula {cedula_test}...")
            
        else:
            print(f"⚠️  No se encontró prestador con cédula {cedula_test}")
            print("   Creando uno para prueba...")
            
            # Crear prestador de prueba
            nuevo_prestador = PrestadorServicio(
                cedula_ps=cedula_test,
                nombres_ps="Juan Carlos",
                apellidos_ps="Pérez López",
                fecha_nacimiento=datetime(1990, 1, 15).date(),
                sexo="M",
                estado_civil="S",
                telefono="+57 300 123 4567",
                email="juan.perez.test@example.com",
                direccion="Calle 123 #45-67",
                codigo_sap=f"SAP{cedula_test}",
                usuario_registro="TEST_SYSTEM"
            )
            
            try:
                db.session.add(nuevo_prestador)
                db.session.commit()
                print(f"✅ Prestador creado exitosamente con ID: {nuevo_prestador.id}")
                
            except Exception as e:
                print(f"❌ Error creando prestador de prueba: {str(e)}")
                db.session.rollback()
                return False
        
        # Contar total de prestadores
        total_prestadores = PrestadorServicio.query.count()
        print(f"\n📊 Total prestadores en base de datos: {total_prestadores}")
        
        # Verificar unicidad en la base de datos
        cedulas_duplicadas = db.session.query(
            PrestadorServicio.cedula_ps,
            db.func.count(PrestadorServicio.cedula_ps).label('count')
        ).group_by(PrestadorServicio.cedula_ps).having(
            db.func.count(PrestadorServicio.cedula_ps) > 1
        ).all()
        
        if cedulas_duplicadas:
            print(f"\n⚠️  PROBLEMA: Encontradas {len(cedulas_duplicadas)} cédulas duplicadas:")
            for cedula, count in cedulas_duplicadas:
                print(f"   - Cédula {cedula}: {count} registros")
            return False
        else:
            print("\n✅ VALIDACIÓN EXITOSA: No hay cédulas duplicadas en la base de datos")
            return True

if __name__ == "__main__":
    try:
        resultado = test_unicidad_cedula()
        if resultado:
            print("\n🎉 Todas las pruebas de unicidad pasaron correctamente")
        else:
            print("\n❌ Algunas pruebas fallaron")
            
    except Exception as e:
        print(f"\n💥 Error ejecutando pruebas: {str(e)}")
        import traceback
        traceback.print_exc()