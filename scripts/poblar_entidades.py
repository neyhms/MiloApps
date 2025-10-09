import sys
import os
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from models import db, TalentEntidad
from app import MiloAppsApp

app_instance = MiloAppsApp()
app = app_instance.app

entidades = [
    # Profesiones
    dict(tipo_entidad='profesion', nombre='Médico', codigo='PR001'),
    dict(tipo_entidad='profesion', nombre='Ingeniero', codigo='PR002'),
    dict(tipo_entidad='profesion', nombre='Psicólogo', codigo='PR003'),
    # Bancos
    dict(tipo_entidad='banco', nombre='Banco Nacional', codigo='BN001'),
    dict(tipo_entidad='banco', nombre='Banco Popular', codigo='BN002'),
    # EPS
    dict(tipo_entidad='eps', nombre='EPS Salud Total', codigo='EPS001'),
    dict(tipo_entidad='eps', nombre='EPS Sura', codigo='EPS002'),
    # AFP
    dict(tipo_entidad='afp', nombre='AFP Protección', codigo='AFP001'),
    dict(tipo_entidad='afp', nombre='AFP Porvenir', codigo='AFP002'),
    # ARL
    dict(tipo_entidad='arl', nombre='ARL Colmena', codigo='ARL001'),
    dict(tipo_entidad='arl', nombre='ARL Sura', codigo='ARL002'),
    # Caja de Compensación
    dict(tipo_entidad='caja_compensacion', nombre='Compensar', codigo='CC001'),
    # Operador SS
    dict(tipo_entidad='operador_ss', nombre='Operador Social', codigo='OSS001'),
    # Área Personal
    dict(tipo_entidad='area_personal', nombre='Administrativo', codigo='AP001'),
    dict(tipo_entidad='area_personal', nombre='Operativo', codigo='AP002'),
    # Municipio
    dict(tipo_entidad='municipio', nombre='Bogotá', codigo='MUN001', departamento='Cundinamarca', codigo_dane='11001'),
    dict(tipo_entidad='municipio', nombre='Medellín', codigo='MUN002', departamento='Antioquia', codigo_dane='05001'),
]

with app.app_context():
    for ent in entidades:
        entidad = TalentEntidad(
            tipo_entidad=ent['tipo_entidad'],
            nombre=ent['nombre'],
            codigo=ent.get('codigo'),
            departamento=ent.get('departamento'),
            codigo_dane=ent.get('codigo_dane'),
            activo=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(entidad)
    db.session.commit()
    print('Entidades de ejemplo insertadas correctamente.')
