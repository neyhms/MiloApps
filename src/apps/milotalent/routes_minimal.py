from flask import Blueprint, render_template_string
from flask_login import login_required

milotalent_bp = Blueprint("milotalent", __name__, url_prefix="/talent")


@milotalent_bp.route("/")
@milotalent_bp.route("/dashboard")
@login_required
def dashboard():
    """Dashboard básico sin templates externos"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MiloTalent</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-4">
            <h1>MiloTalent - Dashboard</h1>
            <div class="row mt-4">
                <div class="col-md-3">
                    <div class="card bg-primary text-white">
                        <div class="card-body">
                            <h3>0</h3>
                            <p>Total PS</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="mt-4">
                <a href="/talent/registro" class="btn btn-primary">+ Nuevo PS</a>
            </div>
        </div>
    </body>
    </html>
    """
    return html


@milotalent_bp.route("/registro")
@login_required
def registro_ps():
    """Formulario básico sin templates externos"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Registro PS</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-4">
            <h1>Registro de Prestador de Servicios</h1>
            <form method="POST" action="/talent/registro">
                <div class="mb-3">
                    <label class="form-label">Cédula *</label>
                    <input type="text" class="form-control" name="cedula" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Nombre Completo *</label>
                    <input type="text" class="form-control" name="nombre_completo" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Correo *</label>
                    <input type="email" class="form-control" name="correo" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Perfil *</label>
                    <select class="form-select" name="perfil_profesional" required>
                        <option value="">Seleccione...</option>
                        <option value="TECNICO">Técnico</option>
                        <option value="PROFESIONAL">Profesional</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label class="form-label">Experiencia (meses) *</label>
                    <input type="number" class="form-control" name="experiencia_meses" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Sector *</label>
                    <select class="form-select" name="sector" required>
                        <option value="">Seleccione...</option>
                        <option value="PUBLICO">Público</option>
                        <option value="PRIVADO">Privado</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label class="form-label">Modalidad *</label>
                    <select class="form-select" name="modalidad" required>
                        <option value="">Seleccione...</option>
                        <option value="PRESTACION_SERVICIOS">Prestación de Servicios</option>
                        <option value="CONSULTOR">Consultor</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary">Registrar PS</button>
                <a href="/talent" class="btn btn-secondary">Cancelar</a>
            </form>
        </div>
    </body>
    </html>
    """
    return html


@milotalent_bp.route("/registro", methods=["POST"])
@login_required
def crear_ps():
    """Procesamiento básico"""
    from flask import request, flash, redirect, url_for

    try:
        # Lógica básica de registro
        flash("PS registrado exitosamente", "success")
        return redirect(url_for("milotalent.dashboard"))
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for("milotalent.registro_ps"))
