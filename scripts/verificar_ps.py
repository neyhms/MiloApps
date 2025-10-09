
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from apps.milotalent.models import PrestadorServicio
from models import db
from app import MiloAppsApp

app_instance = MiloAppsApp()
app = app_instance.app

with app.app_context():
    total = PrestadorServicio.query.count()
    print(f"Total PS: {total}")
    for ps in PrestadorServicio.query.all():
        if ps is not None and hasattr(ps, 'cedula_ps'):
            print(f"Cédula: {ps.cedula_ps}, Nombre: {ps.nombre_1} {ps.apellido_1}")
        else:
            print("Registro PS inválido o incompleto:", ps)
