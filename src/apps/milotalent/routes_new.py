
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

)


# Blueprint
milotalent_bp = Blueprint('milotalent', __name__, 
                          url_prefix='/milotalent')

# ========================================
# DETALLE, EDICIÓN Y EXPORTACIÓN DE PS
# ========================================

@milotalent_bp.route('/ps/<int:ps_id>')
@login_required
def ver_ps(ps_id):
    ps = PrestadorServicio.query.get_or_404(ps_id)
    return render_template('milotalent/registro/ver_ps.html', ps=ps)

@milotalent_bp.route('/ps/<int:ps_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_ps(ps_id):
    ps = PrestadorServicio.query.get_or_404(ps_id)
    if request.method == 'POST':
        data = request.form
        ps.cedula_ps = data.get('cedula_ps', ps.cedula_ps)
        ps.nombre_1 = data.get('nombre_1', ps.nombre_1)
        ps.nombre_2 = data.get('nombre_2', ps.nombre_2)
        ps.apellido_1 = data.get('apellido_1', ps.apellido_1)
        ps.apellido_2 = data.get('apellido_2', ps.apellido_2)
        ps.sexo = data.get('sexo', ps.sexo)
        fecha_nacimiento_str = data.get('fecha_nacimiento', None)
        if fecha_nacimiento_str:
            from datetime import datetime
            try:
                ps.fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
            except Exception:
                pass
        ps.mail = data.get('mail', ps.mail)
        ps.telefono = data.get('telefono', ps.telefono)
        ps.direccion = data.get('direccion', ps.direccion)
        ps.pais_residencia = data.get('pais_residencia', ps.pais_residencia)
        ps.codigo_sap = data.get('codigo_sap', ps.codigo_sap)
        ps.estado_civil = data.get('estado_civil', ps.estado_civil)
        ps.rh = data.get('rh', ps.rh)
        ps.discapacidad = data.get('discapacidad', ps.discapacidad)
        ps.identidad_genero = data.get('identidad_genero', ps.identidad_genero)
        ps.raza = data.get('raza', ps.raza)
        ps.no_hijos = data.get('no_hijos', ps.no_hijos)
        ps.tipo_riesgo = data.get('tipo_riesgo', ps.tipo_riesgo)
        ps.cuenta_bancaria = data.get('cuenta_bancaria', ps.cuenta_bancaria)
        ps.tipo_cuenta = data.get('tipo_cuenta', ps.tipo_cuenta)
        ps.nuevo_viejo = data.get('nuevo_viejo', ps.nuevo_viejo)
        # Guardar cambios
        from models import db
        db.session.commit()
        flash('Cambios guardados correctamente.', 'success')
        return redirect(url_for('milotalent.ver_ps', ps_id=ps.id))
    return render_template('milotalent/registro/editar_ps.html', ps=ps)

@milotalent_bp.route('/ps/<int:ps_id>/exportar')
@login_required
def exportar_ps(ps_id):
    ps = PrestadorServicio.query.get_or_404(ps_id)
    # Exportar como JSON simple
    return jsonify(ps.to_dict())


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
    try:
        if request.method == 'POST':
            # Obtener datos del formulario
            data = request.form.to_dict()
            print("=== DEBUG: Datos recibidos del formulario ===")
            for key, value in data.items():
                print(f"{key}: {value}")
            print("=" * 50)

            # VALIDACIÓN DE CAMPOS OBLIGATORIOS
            campos_requeridos = [
                'cedula_ps', 'expedida_id', 'nombre_1', 'apellido_1', 'sexo',
                'codigo_sap', 'fecha_nacimiento', 'ciudad_nacimiento_id', 'direccion',
                'municipio_residencia_id', 'telefono', 'mail', 'profesion_id',
                'estado_civil', 'rh', 'identidad_genero', 'raza', 'banco_id',
                'cuenta_bancaria', 'tipo_cuenta', 'regimen_iva', 'eps_id', 'afp_id',
                'arl_id', 'tipo_riesgo', 'operador_ss_id', 'nuevo_viejo', 'area_personal_id'
            ]
            campos_faltantes = [campo for campo in campos_requeridos if not data.get(campo)]
            if campos_faltantes:
                flash(f"Faltan campos obligatorios: {', '.join(campos_faltantes)}", "error")
                return render_template('milotalent/registro/formulario_new.html')

            # VALIDACIÓN DE UNICIDAD DE CÉDULA Y CÓDIGO SAP
            if PrestadorServicio.query.filter_by(cedula_ps=data['cedula_ps']).first():
                flash("Ya existe un PS registrado con esta cédula", "error")
                return render_template('milotalent/registro/formulario_new.html')
            if PrestadorServicio.query.filter_by(codigo_sap=data['codigo_sap']).first():
                flash("Ya existe un PS registrado con este código SAP", "error")
                return render_template('milotalent/registro/formulario_new.html')

            # Función para convertir campos a int
            def parse_int_field(field, required=True):
                value = data.get(field)
                if value is None or value == '':
                    if required:
                        raise ValueError(f"Campo obligatorio faltante o vacío: {field}")
                    return None
                try:
                    return int(value)
                except Exception:
                    flash(f"Error al convertir el campo {field} a entero", "error")
                    return None
            # ...existing code...
        else:
            # Si es GET, solo mostrar el formulario sin validar
            return render_template('milotalent/registro/formulario_new.html')

        # Crear nuevo PS
        nuevo_ps = PrestadorServicio(
            cedula_ps=data['cedula_ps'],
            expedida_id=parse_int_field('expedida_id'),
            nombre_1=data['nombre_1'],
            nombre_2=data.get('nombre_2', ''),
            apellido_1=data['apellido_1'],
            apellido_2=data.get('apellido_2', ''),
            sexo=data['sexo'],
            codigo_sap=data['codigo_sap'],
            fecha_nacimiento=datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date(),
            ciudad_nacimiento_id=parse_int_field('ciudad_nacimiento_id'),
            pais_nacimiento=data.get('pais_nacimiento', 'CO'),
            direccion=data['direccion'],
            pais_residencia=data.get('pais_residencia', 'CO'),
            municipio_residencia_id=parse_int_field('municipio_residencia_id'),
            telefono=data['telefono'],
            mail=data['mail'],
            profesion_id=parse_int_field('profesion_id'),
            estado_civil=data['estado_civil'],
            no_hijos=parse_int_field('no_hijos', required=False) or 0,
            rh=data['rh'],
            discapacidad=data.get('discapacidad', 'NINGUNA'),
            identidad_genero=data['identidad_genero'],
            raza=data['raza'],
            banco_id=parse_int_field('banco_id'),
            cuenta_bancaria=data['cuenta_bancaria'],
            tipo_cuenta=data['tipo_cuenta'],
            regimen_iva=data['regimen_iva'],
            eps_id=parse_int_field('eps_id'),
            afp_id=parse_int_field('afp_id'),
            arl_id=parse_int_field('arl_id'),
            tipo_riesgo=data['tipo_riesgo'],
            caja_compensacion_id=parse_int_field('caja_compensacion_id', required=False),
            operador_ss_id=parse_int_field('operador_ss_id'),
            nuevo_viejo=data['nuevo_viejo'],
            area_personal_id=parse_int_field('area_personal_id'),
            usuario_registro=str(current_user.id) if current_user.is_authenticated else 'SYSTEM'
        )

        # Guardar en base de datos
        cedula_ps_val = nuevo_ps.cedula_ps
        db.session.add(nuevo_ps)
        db.session.commit()
        # Recuperar el objeto recién insertado
        nuevo_ps_db = PrestadorServicio.query.filter_by(cedula_ps=cedula_ps_val).first()
        # Registrar auditoría
        auditoria = AuditoriaPS(
            ps_id=nuevo_ps_db.id if nuevo_ps_db else None,
            usuario_id=str(current_user.id) if current_user.is_authenticated else 'SYSTEM',
            accion='registro_ps',
            modulo='registro',
            descripcion=f'Registro de nuevo PS: {nuevo_ps_db.nombre_completo if nuevo_ps_db else cedula_ps_val}',
            valores_nuevos=json.dumps(nuevo_ps_db.to_dict() if nuevo_ps_db else {}),
            ip_usuario=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(auditoria)
        db.session.commit()
        flash(f'PS {nuevo_ps_db.nombre_completo if nuevo_ps_db else cedula_ps_val} registrado exitosamente', 'success')
        return redirect(url_for('milotalent.dashboard'))
    except Exception as e:
        db.session.rollback()
        print(f"Error al registrar PS: {e}")
        flash(f"Error al registrar PS: {e}", 'error')
        return render_template('milotalent/registro/formulario_new.html')
    # ...existing code...


@login_required
@milotalent_bp.route('/listado', endpoint='listado')
@login_required
def listado():
    """Listado de PS registrados (paginado)"""
    page = request.args.get('page', 1, type=int)
    filtro_cedula = request.args.get('cedula', '').strip()
    filtro_nombre = request.args.get('nombre', '').strip()
    filtro_sexo = request.args.get('sexo', '')
    filtro_estado = request.args.get('estado', '')
    filtro_area = request.args.get('area', '')

    query = PrestadorServicio.query
    if filtro_cedula:
        query = query.filter(PrestadorServicio.cedula_ps.like(f'%{filtro_cedula}%'))
    if filtro_nombre:
        query = query.filter(
            (PrestadorServicio.nombre_1.like(f'%{filtro_nombre}%')) |
            (PrestadorServicio.apellido_1.like(f'%{filtro_nombre}%'))
        )
    if filtro_sexo:
        query = query.filter_by(sexo=filtro_sexo)
    if filtro_estado:
        query = query.filter_by(nuevo_viejo=filtro_estado)
    if filtro_area:
        query = query.filter_by(area_personal_id=filtro_area)

    prestadores = query.order_by(PrestadorServicio.fecha_registro.desc()).paginate(page=page, per_page=20)

    return render_template(
        'milotalent/listado/prestadores_nuevo.html',
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
