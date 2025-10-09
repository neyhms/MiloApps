#!/usr/bin/env python3
"""
Script de prueba para validar el registro de PS
Utiliza los datos exactos de las imágenes proporcionadas por el usuario
"""

import sys
import os
sys.path.append('src')

from datetime import datetime, date
from flask import Flask
from models import db
from apps.milotalent.models import (
    PrestadorServicio, Sexo, EstadoCivil, TipoCuenta, 
    RegimenIVA, TipoRiesgo, IdentidadGenero, Raza, NuevoViejo, TipoRH
)

def create_test_app():
    """Crear aplicación Flask para pruebas"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/miloapps.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    db.init_app(app)
    return app

def test_registro_ps():
    """Probar el registro de PS con datos de las imágenes"""
    
    print("=" * 60)
    print("🧪 SCRIPT DE PRUEBA - REGISTRO DE PS")
    print("=" * 60)
    
    # Datos exactos de las imágenes
    datos_test = {
        'cedula_ps': '16761740',
        'expedida': 'CALI',
        'sexo': 'M',
        'nombre_1': 'NEY',
        'nombre_2': 'HERNANDO',
        'apellido_1': 'MUNOZ',
        'apellido_2': 'SANCHEZ',
        'fecha_nacimiento': '1968-10-01',
        'ciudad_nacimiento': 'LA UNION',
        'pais_nacimiento': 'CO',  # Formulario envía CO
        'direccion': 'Carrera 76 16-156 Casa B3',
        'municipio_residencia': 'CALI',
        'pais_residencia': 'CO',  # Formulario envía CO
        'telefono': '3152629017',
        'mail': 'neyhms@gmail.com',
        'profesion': 'INGENIERO DE SISTEMAS',
        'estado_civil': 'Casado',
        'no_hijos': 2,
        'rh': 'O+',
        'discapacidad': 'NINGUNA',
        'identidad_genero': 'MASCULINO',
        'raza': 'MESTIZO',
        'banco': 'BANCO DAVIVIENDA',
        'cuenta_bancaria': '026520264104',
        'tipo_cuenta': '02 Cuenta de Ahorros',
        'regimen_iva': '98 RUT Régimen Simplificado',
        'eps': 'SALUD TOTAL',
        'afp': 'OLD MUTUAL',
        'arl': 'LIBERTY ARL',
        'tipo_riesgo': '004 Labores de alto riesgo Clase IV',
        'caja': 'COMFENALCO',
        'operador_ss': 'MI PLANILLA',
        'codigo_sap': '760001',
        'nuevo_viejo': 'N',  # Formulario envía N
        'area_personal': 'PS'  # Formulario envía PS
    }
    
    print("📋 Datos de prueba:")
    print(f"   Nombre: {datos_test['nombre_1']} {datos_test['nombre_2']} {datos_test['apellido_1']} {datos_test['apellido_2']}")
    print(f"   Cédula: {datos_test['cedula_ps']}")
    print(f"   Email: {datos_test['mail']}")
    print(f"   Código SAP: {datos_test['codigo_sap']}")
    print()
    
    # Crear aplicación Flask
    app = create_test_app()
    
    with app.app_context():
        print("🔧 Validando conversión de Enums...")
        
        # Validar cada enum individualmente
        enum_tests = [
            ('sexo', Sexo, datos_test['sexo']),
            ('estado_civil', EstadoCivil, datos_test['estado_civil']),
            ('rh', TipoRH, datos_test['rh']),
            ('identidad_genero', IdentidadGenero, datos_test['identidad_genero']),
            ('raza', Raza, datos_test['raza']),
            ('tipo_cuenta', TipoCuenta, datos_test['tipo_cuenta']),
            ('regimen_iva', RegimenIVA, datos_test['regimen_iva']),
            ('tipo_riesgo', TipoRiesgo, datos_test['tipo_riesgo']),
            ('nuevo_viejo', NuevoViejo, datos_test['nuevo_viejo'])
        ]
        
        for nombre, enum_class, valor in enum_tests:
            try:
                enum_obj = enum_class(valor)
                print(f"   ✅ {nombre}: '{valor}' -> {enum_obj}")
            except ValueError as e:
                print(f"   ❌ {nombre}: Error con '{valor}' - {e}")
                print(f"      Valores válidos: {[e.value for e in enum_class]}")
                return False
        
        print("\n🏗️  Creando objeto PrestadorServicio...")
        
        try:
            # Verificar que no exista ya
            existing = PrestadorServicio.query.filter_by(cedula_ps=datos_test['cedula_ps']).first()
            if existing:
                print(f"   ⚠️  PS con cédula {datos_test['cedula_ps']} ya existe. Eliminando para la prueba...")
                db.session.delete(existing)
                db.session.commit()
            
            # Crear nuevo PS
            nuevo_ps = PrestadorServicio(
                cedula_ps=datos_test['cedula_ps'],
                expedida=datos_test['expedida'],
                nombre_1=datos_test['nombre_1'],
                nombre_2=datos_test['nombre_2'],
                apellido_1=datos_test['apellido_1'],
                apellido_2=datos_test['apellido_2'],
                sexo=Sexo(datos_test['sexo']),
                codigo_sap=datos_test['codigo_sap'],
                fecha_nacimiento=datetime.strptime(datos_test['fecha_nacimiento'], '%Y-%m-%d').date(),
                ciudad_nacimiento=datos_test['ciudad_nacimiento'],
                pais_nacimiento=datos_test['pais_nacimiento'],
                direccion=datos_test['direccion'],
                pais_residencia=datos_test['pais_residencia'],
                municipio_residencia=datos_test['municipio_residencia'],
                telefono=datos_test['telefono'],
                mail=datos_test['mail'],
                profesion=datos_test['profesion'],
                estado_civil=EstadoCivil(datos_test['estado_civil']),
                no_hijos=datos_test['no_hijos'],
                rh=TipoRH(datos_test['rh']),
                discapacidad=datos_test['discapacidad'],
                identidad_genero=IdentidadGenero(datos_test['identidad_genero']),
                raza=Raza(datos_test['raza']),
                banco=datos_test['banco'],
                cuenta_bancaria=datos_test['cuenta_bancaria'],
                tipo_cuenta=TipoCuenta(datos_test['tipo_cuenta']),
                regimen_iva=RegimenIVA(datos_test['regimen_iva']),
                eps=datos_test['eps'],
                afp=datos_test['afp'],
                arl=datos_test['arl'],
                tipo_riesgo=TipoRiesgo(datos_test['tipo_riesgo']),
                caja=datos_test['caja'],
                operador_ss=datos_test['operador_ss'],
                nuevo_viejo=NuevoViejo(datos_test['nuevo_viejo']),
                area_personal=datos_test['area_personal'],
                usuario_registro='TEST_SCRIPT'
            )
            
            print("   ✅ Objeto PrestadorServicio creado exitosamente")
            
            # Guardar en base de datos
            print("\n💾 Guardando en base de datos...")
            db.session.add(nuevo_ps)
            db.session.commit()
            print("   ✅ PS guardado exitosamente en la base de datos")
            
            # Verificar que se guardó correctamente
            print("\n🔍 Verificando registro en base de datos...")
            ps_verificacion = PrestadorServicio.query.filter_by(cedula_ps=datos_test['cedula_ps']).first()
            
            if ps_verificacion:
                print(f"   ✅ PS encontrado en BD:")
                print(f"      ID: {ps_verificacion.id}")
                print(f"      Nombre: {ps_verificacion.nombre_completo}")
                print(f"      Cédula: {ps_verificacion.cedula_ps}")
                print(f"      Email: {ps_verificacion.mail}")
                print(f"      SAP: {ps_verificacion.codigo_sap}")
                print(f"      Fecha registro: {ps_verificacion.fecha_registro}")
                
                # Estadísticas
                total_ps = PrestadorServicio.query.count()
                ps_nuevos = PrestadorServicio.query.filter_by(nuevo_viejo=NuevoViejo.NUEVO).count()
                
                print("\n📊 Estadísticas actuales:")
                print(f"   Total PS: {total_ps}")
                print(f"   PS Nuevos: {ps_nuevos}")
                
                print("\n🎉 ¡PRUEBA EXITOSA!")
                print("   El formulario web debería funcionar correctamente ahora.")
                return True
            else:
                print("   ❌ No se encontró el PS en la base de datos")
                return False
                
        except Exception as e:
            print(f"   ❌ Error al crear PS: {e}")
            import traceback
            print(f"   Traceback: {traceback.format_exc()}")
            return False

if __name__ == "__main__":
    success = test_registro_ps()
    if success:
        print("\n✅ RESULTADO: Todos los tests pasaron exitosamente")
        print("💡 El formulario web debería funcionar sin problemas")
    else:
        print("\n❌ RESULTADO: Falló la prueba")
        print("💡 Revisar los errores mostrados arriba")
    
    print("=" * 60)