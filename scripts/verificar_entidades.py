import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from models import db
from app import MiloAppsApp
from models import TalentEntidad

app_instance = MiloAppsApp()
app = app_instance.app

with app.app_context():
    total = TalentEntidad.query.count()
    print(f"Total entidades: {total}")
    for entidad in TalentEntidad.query.limit(10).all():
        print(f"ID: {entidad.id}, Nombre: {entidad.nombre}")
    if total == 0:
        print("La tabla de entidades está vacía.")
