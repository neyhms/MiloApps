"""
MiloTalent - Rutas actualizadas para nueva estructura
Sistema de Registro de Prestadores de Servicios
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
import json

from models import db
from .models import (
    PrestadorServicio, 
    AuditoriaPS,
    Municipio
)

# Blueprint
milotalent_bp = Blueprint('milotalent', __name__, 
                          url_prefix='/milotalent')


# ========================================
# DASHBOARD
# ========================================

@milotalent_bp.route('/')
@milotalent_bp.route('/api/verificar-cedula')
@login_required
def verificar_cedula():
    """API endpoint para verificar si una cédula ya existe."""
    cedula = request.args.get('cedula', '').strip()
    
    if not cedula:
        return jsonify({'error': 'Cédula requerida'}), 400
    
    # Buscar prestador existente con esa cédula
    prestador_existente = PrestadorServicio.query.filter_by(cedula_ps=cedula).first()
    
    if prestador_existente:
        return jsonify({
            'existe': True,
            'nombre': prestador_existente.nombre_completo,
            'cedula': cedula
        })
    else:
        return jsonify({
            'existe': False,
            'cedula': cedula
        })

@milotalent_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal con nueva estructura"""
    
    # Estadísticas simples
    total_ps = PrestadorServicio.query.count()
    ps_nuevos = PrestadorServicio.query.filter_by(nuevo_viejo='N').count()
    ps_viejos = PrestadorServicio.query.filter_by(nuevo_viejo='V').count()
    
    return render_template(
        'milotalent/dashboard_new.html',
        total_ps=total_ps,
        ps_nuevos=ps_nuevos,
        ps_viejos=ps_viejos,
        cdp_disponible=0
    )


# ========================================
# REGISTRO DE PS
# ========================================

@milotalent_bp.route('/crear-ps', methods=['GET', 'POST'])
@login_required
def crear_ps():
    """Crear nuevo PS con nueva estructura"""
    # Usar app.logger en lugar de print
    from flask import current_app
    current_app.logger.info(f"=== RUTA CREAR_PS LLAMADA ===")
    current_app.logger.info(f"Método: {request.method}")
    current_app.logger.info(f"Content-Type: {request.content_type}")
    current_app.logger.info(f"Form data keys: {list(request.form.keys())}")
    current_app.logger.info("=" * 40)
    
    if request.method == 'GET':
        return render_template('milotalent/registro/formulario_new.html')
        
    try:
        # Obtener datos del formulario
        data = request.form.to_dict()
        
        # DEBUG: Imprimir datos recibidos
        print("=== DEBUG: Datos recibidos del formulario ===")
        for key, value in data.items():
            print(f"{key}: {value}")
        print("=" * 50)
        
        # VALIDACIÓN DE UNICIDAD DE CÉDULA
        cedula_existente = PrestadorServicio.query.filter_by(
            cedula_ps=data.get('cedula_ps', '').strip()
        ).first()
        
        if cedula_existente:
            flash(
                f'Ya existe un prestador registrado con la cédula {data.get("cedula_ps")}. '
                f'Nombre: {cedula_existente.nombre_1} {cedula_existente.apellido_1}',
                'error'
            )
            return render_template('milotalent/registro/formulario_new.html')
        
        # VALIDACIÓN DE UNICIDAD DE CÓDIGO SAP
        sap_existente = PrestadorServicio.query.filter_by(
            codigo_sap=data.get('codigo_sap', '').strip()
        ).first()
        
        if sap_existente:
            flash(
                f'Ya existe un prestador registrado con el código SAP {data.get("codigo_sap")}. '
                f'Cédula: {sap_existente.cedula_ps}',
                'error'
            )
            return render_template('milotalent/registro/formulario_new.html')
        
        # Validaciones básicas
        campos_requeridos = [
            'cedula_ps', 'expedida', 'nombre_1', 'apellido_1', 'sexo',
            'codigo_sap', 'fecha_nacimiento', 'ciudad_nacimiento', 'direccion',
            'municipio_residencia', 'telefono', 'mail', 'profesion', 
            'estado_civil', 'rh', 'identidad_genero', 'raza', 'banco',
            'cuenta_bancaria', 'tipo_cuenta', 'regimen_iva', 'eps', 'afp',
            'arl', 'tipo_riesgo', 'operador_ss', 'nuevo_viejo', 'area_personal'
        ]
        
        campos_faltantes = [campo for campo in campos_requeridos if not data.get(campo)]
        if campos_faltantes:
            flash(f"Faltan campos obligatorios: {', '.join(campos_faltantes)}", "error")
            return render_template('milotalent/registro/formulario_new.html')
        
        # Verificar que la cédula no exista
        if PrestadorServicio.query.filter_by(cedula_ps=data['cedula_ps']).first():
            flash("Ya existe un PS registrado con esta cédula", "error")
            return render_template('milotalent/registro/formulario_new.html')
        
        # Verificar que el código SAP no exista
        if PrestadorServicio.query.filter_by(codigo_sap=data['codigo_sap']).first():
            flash("Ya existe un PS registrado con este código SAP", "error")
            return render_template('milotalent/registro/formulario_new.html')
        
        # Crear nuevo PS con validación de enums
        try:
            nuevo_ps = PrestadorServicio(
                cedula_ps=data['cedula_ps'],
                expedida_id=int(data['expedida_id']),
                nombre_1=data['nombre_1'],
                nombre_2=data.get('nombre_2', ''),
                apellido_1=data['apellido_1'],
                apellido_2=data.get('apellido_2', ''),
                sexo=data['sexo'],
                codigo_sap=data['codigo_sap'],
                fecha_nacimiento=datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date(),
                ciudad_nacimiento_id=int(data['ciudad_nacimiento_id']),
                pais_nacimiento=data.get('pais_nacimiento', 'CO'),
                direccion=data['direccion'],
                pais_residencia=data.get('pais_residencia', 'CO'),
                municipio_residencia_id=int(data['municipio_residencia_id']),
                telefono=data['telefono'],
                mail=data['mail'],
                profesion=data['profesion'],
                estado_civil=data['estado_civil'],
                no_hijos=int(data.get('no_hijos', 0)),
                rh=data['rh'],
                discapacidad=data.get('discapacidad', 'NINGUNA'),
                identidad_genero=data['identidad_genero'],
                raza=data['raza'],
                banco=data['banco'],
                cuenta_bancaria=data['cuenta_bancaria'],
                tipo_cuenta=data['tipo_cuenta'],
                regimen_iva=data['regimen_iva'],
                eps=data['eps'],
                afp=data['afp'],
                arl=data['arl'],
                tipo_riesgo=data['tipo_riesgo'],
                caja=data.get('caja', ''),
                operador_ss=data['operador_ss'],
                nuevo_viejo=data['nuevo_viejo'],
                area_personal=data['area_personal'],
                usuario_registro=str(current_user.id) if current_user.is_authenticated else 'SYSTEM'
            )
        except ValueError as enum_error:
            print(f"Error al convertir Enum: {enum_error}")
            flash(f'Error en los datos del formulario: {str(enum_error)}', 'error')
            return render_template('milotalent/registro/formulario_new.html')
        
        # Guardar en base de datos
        db.session.add(nuevo_ps)
        db.session.commit()
        
        # Registrar auditoría
        auditoria = AuditoriaPS(
            ps_id=nuevo_ps.id,
            usuario_id=str(current_user.id) if current_user.is_authenticated else 'SYSTEM',
            accion='registro_ps',
            modulo='registro',
            descripcion=f'Registro de nuevo PS: {nuevo_ps.nombre_completo}',
            valores_nuevos=json.dumps(nuevo_ps.to_dict()),
            ip_usuario=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        
        db.session.add(auditoria)
        db.session.commit()
        
        flash(f'PS {nuevo_ps.nombre_completo} registrado exitosamente', 'success')
        return redirect(url_for('milotalent.dashboard'))
        
    except Exception as e:
        db.session.rollback()
        print(f"=== DEBUG: Error al registrar PS ===")
        print(f"Error: {str(e)}")
        print(f"Tipo de error: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        print("=" * 50)
        flash(f'Error al registrar PS: {str(e)}', 'error')
        return render_template('milotalent/registro/formulario_new.html')


# ========================================
# LISTADO DE PS
# ========================================

@milotalent_bp.route('/listado')
@login_required
def listado():
    """Mostrar listado de todos los PS"""
    
    # Paginación
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Filtros
    filtro_cedula = request.args.get('cedula', '').strip()
    filtro_nombre = request.args.get('nombre', '').strip()
    filtro_sexo = request.args.get('sexo', '')
    filtro_estado = request.args.get('estado', '')
    filtro_area = request.args.get('area', '')
    
    # Query base
    query = PrestadorServicio.query
    
    # Aplicar filtros
    if filtro_cedula:
        query = query.filter(PrestadorServicio.cedula_ps.like(f'%{filtro_cedula}%'))
    
    if filtro_nombre:
        # Buscar en nombre_1, nombre_2, apellido_1, apellido_2
        nombre_filter = (
            PrestadorServicio.nombre_1.like(f'%{filtro_nombre}%') |
            PrestadorServicio.nombre_2.like(f'%{filtro_nombre}%') |
            PrestadorServicio.apellido_1.like(f'%{filtro_nombre}%') |
            PrestadorServicio.apellido_2.like(f'%{filtro_nombre}%')
        )
        query = query.filter(nombre_filter)
    
    if filtro_sexo:
        query = query.filter_by(sexo=filtro_sexo)
    
    if filtro_estado:
        query = query.filter_by(nuevo_viejo=filtro_estado)
    
    if filtro_area:
        query = query.filter_by(area_personal=filtro_area)
    
    # Ordenar por fecha de registro descendente
    query = query.order_by(PrestadorServicio.fecha_registro.desc())
    
    prestadores = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return render_template(
        'milotalent/listado/prestadores.html',
        prestadores=prestadores,
        filtro_cedula=filtro_cedula,
        filtro_nombre=filtro_nombre,
        filtro_sexo=filtro_sexo,
        filtro_estado=filtro_estado,
        filtro_area=filtro_area
    )


# ========================================
# API ENDPOINTS
# ========================================

@milotalent_bp.route('/api/stats')
@login_required
def api_stats():
    """API con estadísticas actualizadas"""
    stats = {
        'total_ps': PrestadorServicio.query.count(),
        'ps_nuevos': PrestadorServicio.query.filter_by(nuevo_viejo='N').count(),
        'ps_viejos': PrestadorServicio.query.filter_by(nuevo_viejo='V').count(),
        'hombres': PrestadorServicio.query.filter_by(sexo='M').count(),
        'mujeres': PrestadorServicio.query.filter_by(sexo='F').count(),
    }
    return jsonify(stats)


@milotalent_bp.route('/api/prestadores')
@login_required
def api_prestadores():
    """API para obtener lista de prestadores"""
    prestadores = PrestadorServicio.query.all()
    return jsonify({
        'prestadores': [ps.to_dict() for ps in prestadores],
        'total': len(prestadores)
    })