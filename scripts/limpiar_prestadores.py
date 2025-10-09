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
    print(f"Registros a eliminar: {total}")
    PrestadorServicio.query.delete()
    db.session.commit()
    print("Todos los registros de PrestadorServicio han sido eliminados.")
