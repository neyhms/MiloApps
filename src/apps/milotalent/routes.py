"""
MiloTalent - Rutas y Controladores
Sistema de Contratación de Prestadores de Servicios

Implementa los 9 módulos funcionales definidos en la arquitectura:
1. Registro y Validación de PS
2. Diagnóstico y Ubicación del PS
3. Gestión Presupuestal y CDP
4. Generación de Expediente Precontractual
5. Autorizaciones y Cronogramas
6. Publicación en SECOP II
7. Registro en SAP-HCM y ARL
8. Base de Datos Institucional de PS
9. Alertas y Seguimiento
"""

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
import uuid

from . import milotalent_bp
from .models import (
    PrestadorServicio,
    CDP,
    Expediente,
    HistorialContrato,
    DocumentoPS,
    Alerta,
    AuditoriaPS,
    EstadoProceso,
    SectorExperiencia,
    ModalidadContrato,
    EstadoCDP,
    TipoAlerta,
)
from models import db


# ========================================
# DASHBOARD PRINCIPAL
# ========================================


@milotalent_bp.route("/")
@milotalent_bp.route("/dashboard")
@login_required
def dashboard():
    """
    Dashboard principal de MiloTalent
    Vista general del sistema con métricas clave
    """
    # Estadísticas generales
    total_ps = PrestadorServicio.query.count()
    ps_activos = PrestadorServicio.query.filter_by(estado=EstadoProceso.ACTIVO).count()
    ps_en_proceso = PrestadorServicio.query.filter(
        PrestadorServicio.estado.in_(
            [
                EstadoProceso.REGISTRO,
                EstadoProceso.VALIDACION,
                EstadoProceso.DIAGNOSTICO,
                EstadoProceso.EXPEDIENTE,
            ]
        )
    ).count()

    # CDP disponible
    cdp_disponible = (
        db.session.query(db.func.sum(CDP.valor_disponible))
        .filter(CDP.estado == EstadoCDP.DISPONIBLE)
        .scalar()
        or 0
    )

    # Alertas activas
    alertas_activas = Alerta.query.filter_by(estado="activa").count()
    alertas_urgentes = (
        Alerta.query.filter_by(estado="activa")
        .filter(Alerta.fecha_vencimiento <= datetime.now())
        .count()
    )

    # PS recientes
    ps_recientes = (
        PrestadorServicio.query.order_by(PrestadorServicio.fecha_registro.desc())
        .limit(5)
        .all()
    )

    # Alertas recientes
    alertas_recientes = (
        Alerta.query.filter_by(estado="activa")
        .order_by(Alerta.fecha_creacion.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "milotalent/dashboard_clean.html",
        total_ps=total_ps,
        ps_activos=ps_activos,
        ps_en_proceso=ps_en_proceso,
        cdp_disponible=cdp_disponible,
        alertas_activas=alertas_activas,
        alertas_urgentes=alertas_urgentes,
        ps_recientes=ps_recientes,
        alertas_recientes=alertas_recientes,
    )


# ========================================
# MÓDULO 1: REGISTRO Y VALIDACIÓN DE PS
# ========================================


@milotalent_bp.route("/registro")
@login_required
def registro_ps():
    """Formulario de registro de PS"""
    return render_template("milotalent/registro/formulario_clean.html")


@milotalent_bp.route("/registro", methods=["POST"])
@login_required
def crear_ps():
    """Crear nuevo prestador de servicios"""
    try:
        # Validar que no exista la cédula
        cedula = request.form.get("cedula")
        if PrestadorServicio.query.filter_by(cedula=cedula).first():
            flash("Ya existe un PS registrado con esta cédula", "error")
            return redirect(url_for("milotalent.registro_ps"))

        # Crear nuevo PS
        ps = PrestadorServicio(
            cedula=cedula,
            nombre_completo=request.form.get("nombre_completo"),
            correo=request.form.get("correo"),
            telefono=request.form.get("telefono", ""),
            perfil_profesional=request.form.get("perfil_profesional"),
            experiencia_total_meses=int(request.form.get("experiencia_meses", 0)),
            sector_experiencia=SectorExperiencia(request.form.get("sector")),
            modalidad=ModalidadContrato(request.form.get("modalidad")),
            usuario_registro=current_user.id,
        )

        db.session.add(ps)
        db.session.commit()

        # Registrar auditoría
        auditoria = AuditoriaPS(
            ps_id=ps.id_ps,
            usuario_id=current_user.id,
            accion="crear_ps",
            modulo="registro",
            descripcion=f"PS registrado: {ps.nombre_completo}",
            ip_usuario=request.remote_addr,
        )
        db.session.add(auditoria)
        db.session.commit()

        flash(f"PS {ps.nombre_completo} registrado exitosamente", "success")
        return redirect(url_for("milotalent.validacion_ps", ps_id=ps.id_ps))

    except Exception as e:
        db.session.rollback()
        flash(f"Error al registrar PS: {str(e)}", "error")
        return redirect(url_for("milotalent.registro_ps"))


@milotalent_bp.route("/validacion/<ps_id>")
@login_required
def validacion_ps(ps_id):
    """Pantalla de validación de documentos"""
    ps = PrestadorServicio.query.get_or_404(ps_id)
    documentos = DocumentoPS.query.filter_by(ps_id=ps_id).all()

    return render_template(
        "milotalent/registro/validacion.html", ps=ps, documentos=documentos
    )


# ========================================
# MÓDULO 2: DIAGNÓSTICO Y UBICACIÓN DEL PS
# ========================================


@milotalent_bp.route("/diagnostico")
@login_required
def diagnostico_lista():
    """Lista de PS para diagnóstico"""
    ps_pendientes = PrestadorServicio.query.filter(
        PrestadorServicio.estado.in_(
            [EstadoProceso.VALIDACION, EstadoProceso.DIAGNOSTICO]
        )
    ).all()

    return render_template(
        "milotalent/diagnostico/lista.html", ps_pendientes=ps_pendientes
    )


@milotalent_bp.route("/diagnostico/<ps_id>")
@login_required
def diagnostico_ps(ps_id):
    """Panel de evaluación y diagnóstico de PS"""
    ps = PrestadorServicio.query.get_or_404(ps_id)

    # Calcular honorarios sugeridos según GVAL (mock)
    honorarios_sugeridos = calcular_honorarios_gval(ps)

    return render_template(
        "milotalent/diagnostico/evaluacion.html",
        ps=ps,
        honorarios_sugeridos=honorarios_sugeridos,
    )


@milotalent_bp.route("/diagnostico/<ps_id>", methods=["POST"])
@login_required
def actualizar_diagnostico(ps_id):
    """Actualizar diagnóstico y ubicación del PS"""
    ps = PrestadorServicio.query.get_or_404(ps_id)

    try:
        # Actualizar información del diagnóstico
        ps.dependencia_asignada = request.form.get("dependencia")
        ps.objeto_contractual = request.form.get("objeto_contractual")
        ps.actividades_especificas = request.form.get("actividades")
        ps.valor_mensual = float(request.form.get("valor_mensual", 0))
        ps.valor_total = float(request.form.get("valor_total", 0))
        ps.supervisor_designado = request.form.get("supervisor")
        ps.estado = EstadoProceso.PRESUPUESTO

        db.session.commit()

        # Auditoría
        auditoria = AuditoriaPS(
            ps_id=ps.id_ps,
            usuario_id=current_user.id,
            accion="diagnostico_completado",
            modulo="diagnostico",
            descripcion=f"Diagnóstico completado para {ps.nombre_completo}",
            ip_usuario=request.remote_addr,
        )
        db.session.add(auditoria)
        db.session.commit()

        flash("Diagnóstico actualizado exitosamente", "success")
        return redirect(url_for("milotalent.gestion_cdp"))

    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar diagnóstico: {str(e)}", "error")
        return redirect(url_for("milotalent.diagnostico_ps", ps_id=ps_id))


# ========================================
# MÓDULO 3: GESTIÓN PRESUPUESTAL Y CDP
# ========================================


@milotalent_bp.route("/cdp")
@login_required
def gestion_cdp():
    """Panel de gestión de CDP"""
    cdps = CDP.query.all()
    ps_sin_cdp = PrestadorServicio.query.filter(
        PrestadorServicio.estado == EstadoProceso.PRESUPUESTO,
        PrestadorServicio.cdp_id.is_(None),
    ).all()

    return render_template(
        "milotalent/cdp/gestion.html", cdps=cdps, ps_sin_cdp=ps_sin_cdp
    )


@milotalent_bp.route("/cdp/crear", methods=["POST"])
@login_required
def crear_cdp():
    """Crear nuevo CDP"""
    try:
        cdp = CDP(
            numero_cdp=request.form.get("numero_cdp"),
            rubro=request.form.get("rubro"),
            dependencia=request.form.get("dependencia"),
            valor_inicial=float(request.form.get("valor_inicial")),
            valor_disponible=float(request.form.get("valor_inicial")),
            vigencia=int(request.form.get("vigencia")),
            fecha_emision=datetime.strptime(
                request.form.get("fecha_emision"), "%Y-%m-%d"
            ).date(),
            fecha_vencimiento=datetime.strptime(
                request.form.get("fecha_vencimiento"), "%Y-%m-%d"
            ).date(),
            usuario_registro=current_user.id,
        )

        db.session.add(cdp)
        db.session.commit()

        flash("CDP creado exitosamente", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error al crear CDP: {str(e)}", "error")

    return redirect(url_for("milotalent.gestion_cdp"))


@milotalent_bp.route("/cdp/asignar", methods=["POST"])
@login_required
def asignar_cdp():
    """Asignar CDP a PS"""
    try:
        ps_id = request.form.get("ps_id")
        cdp_id = request.form.get("cdp_id")

        ps = PrestadorServicio.query.get_or_404(ps_id)
        cdp = CDP.query.get_or_404(cdp_id)

        # Verificar disponibilidad
        if not cdp.puede_comprometer(ps.valor_total):
            flash("CDP no tiene suficiente disponibilidad", "error")
            return redirect(url_for("milotalent.gestion_cdp"))

        # Asignar CDP
        ps.cdp_id = cdp_id
        ps.estado = EstadoProceso.EXPEDIENTE

        # Actualizar disponibilidad del CDP
        cdp.valor_disponible -= ps.valor_total
        cdp.valor_comprometido += ps.valor_total

        if cdp.valor_disponible <= 0:
            cdp.estado = EstadoCDP.COMPROMETIDO

        db.session.commit()

        flash(f"CDP asignado exitosamente a {ps.nombre_completo}", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error al asignar CDP: {str(e)}", "error")

    return redirect(url_for("milotalent.gestion_cdp"))


# ========================================
# MÓDULO 4: GENERACIÓN DE EXPEDIENTE PRECONTRACTUAL
# ========================================


@milotalent_bp.route("/expedientes")
@login_required
def expedientes_lista():
    """Lista de expedientes precontractuales"""
    expedientes = Expediente.query.join(PrestadorServicio).all()
    ps_sin_expediente = (
        PrestadorServicio.query.filter(
            PrestadorServicio.estado == EstadoProceso.EXPEDIENTE
        )
        .filter(~PrestadorServicio.expedientes.any())
        .all()
    )

    return render_template(
        "milotalent/expedientes/lista.html",
        expedientes=expedientes,
        ps_sin_expediente=ps_sin_expediente,
    )


@milotalent_bp.route("/expediente/generar/<ps_id>")
@login_required
def generar_expediente(ps_id):
    """Generar expediente precontractual"""
    ps = PrestadorServicio.query.get_or_404(ps_id)

    try:
        # Crear expediente
        expediente = Expediente(
            ps_id=ps_id,
            consecutivo=generar_consecutivo_expediente(),
            usuario_responsable=current_user.id,
        )

        db.session.add(expediente)
        db.session.commit()

        # Generar formatos automáticamente
        formatos_generados = generar_formatos_expediente(ps, expediente)

        expediente.formatos_generados = str(formatos_generados)
        db.session.commit()

        flash("Expediente generado exitosamente", "success")
        return redirect(
            url_for("milotalent.ver_expediente", expediente_id=expediente.id_expediente)
        )

    except Exception as e:
        db.session.rollback()
        flash(f"Error al generar expediente: {str(e)}", "error")
        return redirect(url_for("milotalent.expedientes_lista"))


# ========================================
# MÓDULO 8: BASE DE DATOS INSTITUCIONAL DE PS
# ========================================


@milotalent_bp.route("/base-datos")
@login_required
def base_datos_ps():
    """Base de datos institucional de PS"""
    # Filtros
    dependencia = request.args.get("dependencia", "")
    modalidad = request.args.get("modalidad", "")
    estado = request.args.get("estado", "")
    vigencia = request.args.get("vigencia", "")

    # Query base
    query = PrestadorServicio.query

    # Aplicar filtros
    if dependencia:
        query = query.filter(
            PrestadorServicio.dependencia_asignada.contains(dependencia)
        )
    if modalidad:
        query = query.filter(
            PrestadorServicio.modalidad == ModalidadContrato(modalidad)
        )
    if estado:
        query = query.filter(PrestadorServicio.estado == EstadoProceso(estado))

    # Paginación
    page = request.args.get("page", 1, type=int)
    prestadores = query.paginate(page=page, per_page=20, error_out=False)

    # Listas para filtros
    dependencias = db.session.query(
        PrestadorServicio.dependencia_asignada.distinct()
    ).all()

    return render_template(
        "milotalent/base_datos/lista.html",
        prestadores=prestadores,
        dependencias=[d[0] for d in dependencias if d[0]],
        filtros={
            "dependencia": dependencia,
            "modalidad": modalidad,
            "estado": estado,
            "vigencia": vigencia,
        },
    )


@milotalent_bp.route("/prestador/<ps_id>")
@login_required
def ver_prestador(ps_id):
    """Ver detalle completo del prestador"""
    ps = PrestadorServicio.query.get_or_404(ps_id)
    historial = HistorialContrato.query.filter_by(ps_id=ps_id).all()
    documentos = DocumentoPS.query.filter_by(ps_id=ps_id).all()
    auditoria = (
        AuditoriaPS.query.filter_by(ps_id=ps_id)
        .order_by(AuditoriaPS.fecha_accion.desc())
        .limit(10)
        .all()
    )

    return render_template(
        "milotalent/prestador/detalle.html",
        ps=ps,
        historial=historial,
        documentos=documentos,
        auditoria=auditoria,
    )


# ========================================
# MÓDULO 9: ALERTAS Y SEGUIMIENTO
# ========================================


@milotalent_bp.route("/alertas")
@login_required
def alertas_lista():
    """Panel de alertas y seguimiento"""
    alertas_activas = (
        Alerta.query.filter_by(estado="activa")
        .order_by(Alerta.fecha_vencimiento.asc())
        .all()
    )

    alertas_urgentes = [a for a in alertas_activas if a.es_urgente]

    return render_template(
        "milotalent/alertas/panel.html",
        alertas_activas=alertas_activas,
        alertas_urgentes=alertas_urgentes,
    )


# ========================================
# API ENDPOINTS
# ========================================


@milotalent_bp.route("/api/stats")
@login_required
def api_stats():
    """API con estadísticas del dashboard"""
    stats = {
        "total_ps": PrestadorServicio.query.count(),
        "ps_activos": PrestadorServicio.query.filter_by(
            estado=EstadoProceso.ACTIVO
        ).count(),
        "cdp_disponible": float(
            db.session.query(db.func.sum(CDP.valor_disponible))
            .filter(CDP.estado == EstadoCDP.DISPONIBLE)
            .scalar()
            or 0
        ),
        "alertas_activas": Alerta.query.filter_by(estado="activa").count(),
    }
    return jsonify(stats)


# ========================================
# FUNCIONES AUXILIARES
# ========================================


def calcular_honorarios_gval(ps):
    """
    Calcular honorarios según tabla GVAL
    Mock function - implementar lógica real según especificaciones
    """
    # Lógica mock basada en experiencia y perfil
    base = 2500000  # Valor base
    if ps.experiencia_anios > 5:
        base *= 1.3
    elif ps.experiencia_anios > 2:
        base *= 1.15

    if ps.sector_experiencia == SectorExperiencia.PUBLICO:
        base *= 1.1

    return {"mensual": base, "total": base * 11}  # Asumiendo contrato de 11 meses


def generar_consecutivo_expediente():
    """Generar consecutivo único para expediente"""
    año = datetime.now().year
    ultimo = Expediente.query.filter(Expediente.consecutivo.like(f"{año}%")).count()
    return f"{año}-{ultimo + 1:04d}"


def generar_formatos_expediente(ps, expediente):
    """
    Generar formatos del expediente con combinación de correspondencia
    Mock function - implementar generación real de documentos
    """
    formatos = [
        "estudios_previos.docx",
        "proyecto_contrato.docx",
        "cdp_expediente.pdf",
        "certificaciones.pdf",
    ]

    # Aquí iría la lógica real de generación de documentos
    # usando templates y combinación de correspondencia

    return formatos
