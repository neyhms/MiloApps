"""
MiloTalent - Rutas para Gestión de Municipios
Sistema de administración de municipios de Colombia
"""

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime

from . import milotalent_bp
from .models import Municipio, db


@milotalent_bp.route('/admin/municipios')
@login_required
def admin_municipios():
    """Página principal de administración de municipios."""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Filtros
    buscar = request.args.get('buscar', '', type=str).strip()
    departamento = request.args.get('departamento', '', type=str).strip()
    activo = request.args.get('activo', '', type=str).strip()
    
    # Query base
    query = Municipio.query
    
    # Aplicar filtros
    if buscar:
        query = query.filter(
            (Municipio.nombre.contains(buscar)) |
            (Municipio.nombre_completo.contains(buscar))
        )
    
    if departamento:
        query = query.filter(Municipio.departamento == departamento)
    
    if activo:
        query = query.filter(Municipio.activo == (activo == 'true'))
    
    # Ordenar y paginar
    municipios = query.order_by(Municipio.nombre_completo).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Obtener lista de departamentos para filtro
    departamentos = db.session.query(Municipio.departamento).distinct().filter(
        Municipio.activo == True
    ).order_by(Municipio.departamento).all()
    departamentos = [d[0] for d in departamentos]
    
    return render_template(
