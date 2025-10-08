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
        'milotalent/admin/municipios.html',
        municipios=municipios,
        departamentos=departamentos,
        filtros={'buscar': buscar, 'departamento': departamento, 'activo': activo}
    )


@milotalent_bp.route('/admin/municipios/crear', methods=['GET', 'POST'])
@login_required
def crear_municipio():
    """Crear nuevo municipio."""
    if request.method == 'POST':
        data = request.form
        
        # Validaciones
        if not data.get('nombre') or not data.get('departamento'):
            flash('Nombre y departamento son obligatorios', 'error')
            return redirect(url_for('milotalent.crear_municipio'))
        
        # Verificar duplicados
        nombre_completo = f"{data['nombre']} - {data['departamento']}"
        existente = Municipio.query.filter_by(nombre_completo=nombre_completo).first()
        
        if existente:
            flash(f'Ya existe el municipio {nombre_completo}', 'error')
            return redirect(url_for('milotalent.crear_municipio'))
        
        try:
            municipio = Municipio(
                nombre=data['nombre'].strip().upper(),
                departamento=data['departamento'].strip().upper(),
                codigo_dane=data.get('codigo_dane', '').strip() or None,
                nombre_completo=f"{data['nombre'].strip().upper()} - {data['departamento'].strip().upper()}",
                activo=True,
                usuario_creacion=str(current_user.id) if current_user.is_authenticated else 'SYSTEM'
            )
            
            db.session.add(municipio)
            db.session.commit()
            
            flash(f'Municipio {nombre_completo} creado exitosamente', 'success')
            return redirect(url_for('milotalent.admin_municipios'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creando municipio: {str(e)}', 'error')
            return redirect(url_for('milotalent.crear_municipio'))
    
    return render_template('milotalent/admin/crear_municipio.html')


@milotalent_bp.route('/admin/municipios/<int:municipio_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_municipio(municipio_id):
    """Editar municipio existente."""
    municipio = Municipio.query.get_or_404(municipio_id)
    
    if request.method == 'POST':
        data = request.form
        
        # Validaciones
        if not data.get('nombre') or not data.get('departamento'):
            flash('Nombre y departamento son obligatorios', 'error')
            return redirect(url_for('milotalent.editar_municipio', municipio_id=municipio_id))
        
        # Verificar duplicados (excluir el actual)
        nombre_completo = f"{data['nombre']} - {data['departamento']}"
        existente = Municipio.query.filter(
            Municipio.nombre_completo == nombre_completo,
            Municipio.id != municipio_id
        ).first()
        
        if existente:
            flash(f'Ya existe el municipio {nombre_completo}', 'error')
            return redirect(url_for('milotalent.editar_municipio', municipio_id=municipio_id))
        
        try:
            municipio.nombre = data['nombre'].strip().upper()
            municipio.departamento = data['departamento'].strip().upper()
            municipio.codigo_dane = data.get('codigo_dane', '').strip() or None
            municipio.nombre_completo = f"{municipio.nombre} - {municipio.departamento}"
            municipio.activo = 'activo' in data
            
            db.session.commit()
            
            flash(f'Municipio {nombre_completo} actualizado exitosamente', 'success')
            return redirect(url_for('milotalent.admin_municipios'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error actualizando municipio: {str(e)}', 'error')
    
    return render_template('milotalent/admin/editar_municipio.html', municipio=municipio)


@milotalent_bp.route('/admin/municipios/<int:municipio_id>/toggle')
@login_required
def toggle_municipio(municipio_id):
    """Activar/Desactivar municipio."""
    municipio = Municipio.query.get_or_404(municipio_id)
    
    try:
        municipio.activo = not municipio.activo
        db.session.commit()
        
        estado = "activado" if municipio.activo else "desactivado"
        flash(f'Municipio {municipio.nombre_completo} {estado} exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error cambiando estado del municipio: {str(e)}', 'error')
    
    return redirect(url_for('milotalent.admin_municipios'))


@milotalent_bp.route('/api/municipios')
def api_municipios_publico():
    """API para obtener municipios (para dropdowns)."""
    departamento = request.args.get('departamento', '', type=str).strip()
    buscar = request.args.get('buscar', '', type=str).strip()
    
    query = Municipio.query.filter(Municipio.activo == True)
    
    if departamento:
        query = query.filter(Municipio.departamento == departamento)
    
    if buscar:
        query = query.filter(
            (Municipio.nombre.contains(buscar.upper())) |
            (Municipio.nombre_completo.contains(buscar.upper()))
        )
    
    municipios = query.order_by(Municipio.nombre_completo).limit(100).all()
    
    return jsonify([{
        'id': m.id,
        'nombre': m.nombre,
        'departamento': m.departamento,
        'nombre_completo': m.nombre_completo,
        'codigo_dane': m.codigo_dane
    } for m in municipios])


@milotalent_bp.route('/api/departamentos')
@login_required
def api_departamentos():
    """API para obtener lista de departamentos."""
    departamentos = db.session.query(Municipio.departamento).distinct().filter(
        Municipio.activo == True
    ).order_by(Municipio.departamento).all()
    
    return jsonify([d[0] for d in departamentos])