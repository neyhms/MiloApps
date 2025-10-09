"""
Rutas para gestión de entidades administrativas genéricas
Sistema CRUD completo para todas las entidades de Talent
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
import json
from datetime import datetime
from models import db, TalentEntidad, get_entidades_por_tipo

# Blueprint para entidades
entidades_bp = Blueprint('entidades', __name__, url_prefix='/admin/entidades')

# Configuración de tipos de entidad
TIPOS_ENTIDAD = {
    'municipio': {
        'nombre': 'Municipios',
        'singular': 'Municipio',
        'campos_especiales': ['departamento', 'codigo_dane'],
        'obligatorio': True
    },
    'profesion': {
        'nombre': 'Profesiones',
        'singular': 'Profesión',
        'campos_especiales': [],
        'obligatorio': True
    },
    'banco': {
        'nombre': 'Bancos',
        'singular': 'Banco',
        'campos_especiales': ['nit', 'telefono'],
        'obligatorio': True
    },
    'eps': {
        'nombre': 'EPS',
        'singular': 'EPS',
        'campos_especiales': ['nit', 'telefono'],
        'obligatorio': True
    },
    'afp': {
        'nombre': 'AFP',
        'singular': 'AFP',
        'campos_especiales': ['nit', 'telefono'],
        'obligatorio': True
    },
    'arl': {
        'nombre': 'ARL',
        'singular': 'ARL',
        'campos_especiales': ['nit', 'telefono'],
        'obligatorio': True
    },
    'caja_compensacion': {
        'nombre': 'Cajas de Compensación',
        'singular': 'Caja de Compensación',
        'campos_especiales': ['nit', 'telefono'],
        'obligatorio': False
    },
    'operador_ss': {
        'nombre': 'Operadores Seguridad Social',
        'singular': 'Operador Seguridad Social',
        'campos_especiales': ['nit', 'telefono'],
        'obligatorio': True
    },
    'area_personal': {
        'nombre': 'Áreas de Personal',
        'singular': 'Área de Personal',
        'campos_especiales': [],
        'obligatorio': True
    }
}

@entidades_bp.route('/')
@login_required
def admin_entidades():
    """Panel principal de administración de entidades"""
    stats = {}
    
    for tipo, config in TIPOS_ENTIDAD.items():
        stats[tipo] = {
            'total': TalentEntidad.query.filter_by(tipo_entidad=tipo).count(),
            'activos': TalentEntidad.query.filter_by(tipo_entidad=tipo, activo=True).count(),
            'inactivos': TalentEntidad.query.filter_by(tipo_entidad=tipo, activo=False).count(),
            'config': config
        }
    
    return render_template('admin/entidades/index.html', 
                         stats=stats, 
                         tipos=TIPOS_ENTIDAD)

@entidades_bp.route('/<tipo>')
@login_required
def listar_entidades(tipo):
    """Lista entidades de un tipo específico"""
    if tipo not in TIPOS_ENTIDAD:
        flash('Tipo de entidad no válido', 'error')
        return redirect(url_for('entidades.admin_entidades'))
    
    # Parámetros de filtro y paginación
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    buscar = request.args.get('buscar', '')
    solo_activos = request.args.get('activos', '1') == '1'
    
    # Query base
    query = TalentEntidad.query.filter_by(tipo_entidad=tipo)
    
    # Aplicar filtros
    if buscar:
        query = query.filter(TalentEntidad.nombre.ilike(f'%{buscar}%'))
    
    if solo_activos:
        query = query.filter_by(activo=True)
    
    # Ordenar y paginar
    query = query.order_by(TalentEntidad.orden, TalentEntidad.nombre)
    entidades = query.paginate(
        page=page, per_page=per_page, 
        error_out=False
    )
    
    return render_template('admin/entidades/listar.html',
                         entidades=entidades,
                         tipo=tipo,
                         config=TIPOS_ENTIDAD[tipo],
                         buscar=buscar,
                         solo_activos=solo_activos)

@entidades_bp.route('/<tipo>/crear', methods=['GET', 'POST'])
@login_required
def crear_entidad(tipo):
    """Crear nueva entidad"""
    if tipo not in TIPOS_ENTIDAD:
        flash('Tipo de entidad no válido', 'error')
        return redirect(url_for('entidades.admin_entidades'))
    
    if request.method == 'POST':
        try:
            # Validar datos requeridos
            nombre = request.form.get('nombre', '').strip()
            if not nombre:
                flash('El nombre es requerido', 'error')
                return render_template('admin/entidades/crear.html', 
                                     tipo=tipo, config=TIPOS_ENTIDAD[tipo])
            
            # Verificar unicidad
            existe = TalentEntidad.query.filter_by(
                tipo_entidad=tipo,
                nombre=nombre
            ).first()
            
            if existe:
                flash(f'Ya existe una {TIPOS_ENTIDAD[tipo]["singular"].lower()} con ese nombre', 'error')
                return render_template('admin/entidades/crear.html', 
                                     tipo=tipo, config=TIPOS_ENTIDAD[tipo])
            
            # Crear nueva entidad
            entidad = TalentEntidad(
                tipo_entidad=tipo,
                nombre=nombre,
                codigo=request.form.get('codigo', '').strip() or None,
                descripcion=request.form.get('descripcion', '').strip() or None,
                departamento=request.form.get('departamento', '').strip() or None,
                codigo_dane=request.form.get('codigo_dane', '').strip() or None,
                nit=request.form.get('nit', '').strip() or None,
                telefono=request.form.get('telefono', '').strip() or None,
                email=request.form.get('email', '').strip() or None,
                direccion=request.form.get('direccion', '').strip() or None,
                es_obligatorio=TIPOS_ENTIDAD[tipo]['obligatorio'],
                permite_otros='permite_otros' in request.form,
                orden=int(request.form.get('orden', 0)),
                created_by=current_user.id
            )
            
            db.session.add(entidad)
            db.session.commit()
            
            flash(f'{TIPOS_ENTIDAD[tipo]["singular"]} creada exitosamente', 'success')
            return redirect(url_for('entidades.listar_entidades', tipo=tipo))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la entidad: {str(e)}', 'error')
    
    return render_template('admin/entidades/crear.html', 
                         tipo=tipo, config=TIPOS_ENTIDAD[tipo])

@entidades_bp.route('/<tipo>/<int:entidad_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_entidad(tipo, entidad_id):
    """Editar entidad existente"""
    if tipo not in TIPOS_ENTIDAD:
        flash('Tipo de entidad no válido', 'error')
        return redirect(url_for('entidades.admin_entidades'))
    
    entidad = TalentEntidad.query.filter_by(id=entidad_id, tipo_entidad=tipo).first()
    if not entidad:
        flash('Entidad no encontrada', 'error')
        return redirect(url_for('entidades.listar_entidades', tipo=tipo))
    
    if request.method == 'POST':
        try:
            # Validar datos requeridos
            nombre = request.form.get('nombre', '').strip()
            if not nombre:
                flash('El nombre es requerido', 'error')
                return render_template('admin/entidades/editar.html', 
                                     entidad=entidad, tipo=tipo, config=TIPOS_ENTIDAD[tipo])
            
            # Verificar unicidad (excluyendo la entidad actual)
            existe = TalentEntidad.query.filter(
                TalentEntidad.tipo_entidad == tipo,
                TalentEntidad.nombre == nombre,
                TalentEntidad.id != entidad_id
            ).first()
            
            if existe:
                flash(f'Ya existe otra {TIPOS_ENTIDAD[tipo]["singular"].lower()} con ese nombre', 'error')
                return render_template('admin/entidades/editar.html', 
                                     entidad=entidad, tipo=tipo, config=TIPOS_ENTIDAD[tipo])
            
            # Actualizar entidad
            entidad.nombre = nombre
            entidad.codigo = request.form.get('codigo', '').strip() or None
            entidad.descripcion = request.form.get('descripcion', '').strip() or None
            entidad.departamento = request.form.get('departamento', '').strip() or None
            entidad.codigo_dane = request.form.get('codigo_dane', '').strip() or None
            entidad.nit = request.form.get('nit', '').strip() or None
            entidad.telefono = request.form.get('telefono', '').strip() or None
            entidad.email = request.form.get('email', '').strip() or None
            entidad.direccion = request.form.get('direccion', '').strip() or None
            entidad.permite_otros = 'permite_otros' in request.form
            entidad.orden = int(request.form.get('orden', 0))
            entidad.activo = 'activo' in request.form
            entidad.updated_by = current_user.id
            entidad.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            flash(f'{TIPOS_ENTIDAD[tipo]["singular"]} actualizada exitosamente', 'success')
            return redirect(url_for('entidades.listar_entidades', tipo=tipo))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la entidad: {str(e)}', 'error')
    
    return render_template('admin/entidades/editar.html', 
                         entidad=entidad, tipo=tipo, config=TIPOS_ENTIDAD[tipo])

@entidades_bp.route('/<tipo>/<int:entidad_id>/eliminar', methods=['POST'])
@login_required
def eliminar_entidad(tipo, entidad_id):
    """Eliminar (desactivar) entidad"""
    if tipo not in TIPOS_ENTIDAD:
        return jsonify({'error': 'Tipo de entidad no válido'}), 400
    
    entidad = TalentEntidad.query.filter_by(id=entidad_id, tipo_entidad=tipo).first()
    if not entidad:
        return jsonify({'error': 'Entidad no encontrada'}), 404
    
    try:
        # Solo desactivar, no eliminar físicamente
        entidad.activo = False
        entidad.updated_by = current_user.id
        entidad.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{TIPOS_ENTIDAD[tipo]["singular"]} desactivada exitosamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al desactivar la entidad: {str(e)}'}), 500

# ===========================
# APIs PÚBLICAS PARA EL FRONT
# ===========================

@entidades_bp.route('/api/<tipo>')
def api_entidades(tipo):
    """API pública para obtener entidades por tipo"""
    if tipo not in TIPOS_ENTIDAD:
        return jsonify({'error': 'Tipo de entidad no válido'}), 400
    
    try:
        entidades = get_entidades_por_tipo(tipo, activos_solo=True)
        
        return jsonify({
            'success': True,
            'data': [entidad.to_dict() for entidad in entidades],
            'tipo': tipo,
            'total': len(entidades)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@entidades_bp.route('/api/<tipo>/<int:entidad_id>')
def api_entidad_detalle(tipo, entidad_id):
    """API para obtener detalle de una entidad específica"""
    if tipo not in TIPOS_ENTIDAD:
        return jsonify({'error': 'Tipo de entidad no válido'}), 400
    
    entidad = TalentEntidad.query.filter_by(
        id=entidad_id, 
        tipo_entidad=tipo, 
        activo=True
    ).first()
    
    if not entidad:
        return jsonify({'error': 'Entidad no encontrada'}), 404
    
    return jsonify({
        'success': True,
        'data': entidad.to_dict()
    })

@entidades_bp.route('/api/all')
def api_todas_entidades():
    """API para obtener todas las entidades agrupadas por tipo"""
    try:
        resultado = {}
        
        for tipo in TIPOS_ENTIDAD.keys():
            entidades = get_entidades_por_tipo(tipo, activos_solo=True)
            resultado[tipo] = [entidad.to_dict() for entidad in entidades]
        
        return jsonify({
            'success': True,
            'data': resultado,
            'tipos': list(TIPOS_ENTIDAD.keys())
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500