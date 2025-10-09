import sys
import os
from datetime import date
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from apps.milotalent.models import PrestadorServicio
from models import db
from app import MiloAppsApp

app_instance = MiloAppsApp()
app = app_instance.app

with app.app_context():
    ps = PrestadorServicio(
        cedula_ps='1234567890',
        expedida_id=1,
        nombre_1='Copilot',
        nombre_2='Test',
        apellido_1='Demo',
        apellido_2='User',
        sexo='M',
        codigo_sap='SAP001',
        fecha_nacimiento=date(1990, 1, 1),
        ciudad_nacimiento_id=1,
        pais_nacimiento='CO',
        direccion='Calle Falsa 123',
        pais_residencia='CO',
        municipio_residencia_id=1,
        telefono='3001234567',
        mail='copilot@example.com',
        profesion_id=1,
        estado_civil='Soltero',
        no_hijos=0,
        rh='O+',
        discapacidad='NINGUNA',
        identidad_genero='MASCULINO',
        raza='MESTIZO',
        banco_id=1,
        cuenta_bancaria='123456789',
        tipo_cuenta='02 Cuenta de Ahorros',
        regimen_iva='98 RUT Régimen Simplificado',
        eps_id=1,
        afp_id=1,
        arl_id=1,
        tipo_riesgo='001 Labores administrativas Clase I',
        caja_compensacion_id=None,
        operador_ss_id=1,
        nuevo_viejo='N',
        area_personal_id=1,
        usuario_registro='SYSTEM'
    )
    db.session.add(ps)
    db.session.commit()
    print('PS de prueba insertado correctamente.')
