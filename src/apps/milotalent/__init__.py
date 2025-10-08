"""
MiloTalent - Sistema de Contratación de Prestadores de Servicios
Blueprint principal para el módulo de gestión de talento
"""

from flask import Blueprint

# Crear blueprint de MiloTalent
milotalent_bp = Blueprint(
    "milotalent",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/milotalent",
)

# Importar rutas después de crear el blueprint para evitar imports circulares
from . import routes_new
from . import municipios
