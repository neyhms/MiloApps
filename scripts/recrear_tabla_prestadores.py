import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from models import db
from app import MiloAppsApp
from apps.milotalent.models import PrestadorServicio

app_instance = MiloAppsApp()
app = app_instance.app

with app.app_context():
    print('Eliminando tabla talent_prestadores_new...')
    db.drop_all()
    db.create_all()
    print('Tabla talent_prestadores_new recreada correctamente.')
