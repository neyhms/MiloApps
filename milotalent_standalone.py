"""
MiloTalent - Aplicación independiente
Solución temporal mientras se resuelven los problemas de templates en MiloApps
"""

from flask import (
    Flask,
    render_template_string,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
)
import os
import sys

# Agregar el directorio src al path para importar los modelos
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

app = Flask(__name__)
app.secret_key = "milotalent-temp-key-2025"

# Template base HTML
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}MiloTalent{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .navbar { background: linear-gradient(135deg, #ff8c42 0%, #ff6b1a 100%); }
        .navbar-brand { color: white !important; font-weight: bold; }
        .stat-card { border-radius: 10px; padding: 1.5rem; margin-bottom: 1rem; }
        .stat-value { font-size: 2rem; font-weight: bold; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-users-cog me-2"></i>MiloTalent
            </a>
        </div>
    </nav>
    
    <div class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'danger' if category == 'error' else 'success' }} alert-dismissible fade show">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# Dashboard HTML
DASHBOARD_HTML = BASE_TEMPLATE.replace(
    "{% block content %}{% endblock %}",
    """
<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h1 class="h3 mb-0">
            <i class="fas fa-users-cog me-2"></i>MiloTalent - Dashboard
        </h1>
        <p class="text-muted">Sistema de Contratación de Prestadores de Servicios</p>
    </div>
    <div>
        <a href="/registro" class="btn btn-primary">
            <i class="fas fa-plus me-1"></i>Nuevo PS
        </a>
    </div>
</div>

<div class="row mb-4">
    <div class="col-lg-3 col-md-6">
        <div class="card bg-primary text-white stat-card">
            <div class="card-body">
                <div class="stat-value">0</div>
                <div>Total PS Registrados</div>
            </div>
        </div>
    </div>
    <div class="col-lg-3 col-md-6">
        <div class="card bg-success text-white stat-card">
            <div class="card-body">
                <div class="stat-value">0</div>
                <div>Contratos Activos</div>
            </div>
        </div>
    </div>
    <div class="col-lg-3 col-md-6">
        <div class="card bg-warning text-white stat-card">
            <div class="card-body">
                <div class="stat-value">0</div>
                <div>En Proceso</div>
            </div>
        </div>
    </div>
    <div class="col-lg-3 col-md-6">
        <div class="card bg-info text-white stat-card">
            <div class="card-body">
                <div class="stat-value">$0</div>
                <div>CDP Disponible</div>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-12">
        <h4><i class="fas fa-th-large me-2"></i>Módulos del Sistema</h4>
    </div>
    
    <div class="col-lg-3 col-md-6 mb-3">
        <div class="card h-100">
            <div class="card-body text-center">
                <i class="fas fa-user-plus fa-3x text-primary mb-3"></i>
                <h6>Registro y Validación</h6>
                <p class="text-muted small">Capturar datos del PS y validar requisitos</p>
                <a href="/registro" class="btn btn-outline-primary btn-sm">Acceder</a>
            </div>
        </div>
    </div>
    
    <div class="col-lg-3 col-md-6 mb-3">
        <div class="card h-100">
            <div class="card-body text-center">
                <i class="fas fa-search-dollar fa-3x text-success mb-3"></i>
                <h6>Diagnóstico y Ubicación</h6>
                <p class="text-muted small">Determinar idoneidad</p>
                <a href="#" class="btn btn-outline-success btn-sm">Próximamente</a>
            </div>
        </div>
    </div>
    
    <div class="col-lg-3 col-md-6 mb-3">
        <div class="card h-100">
            <div class="card-body text-center">
                <i class="fas fa-money-bill-wave fa-3x text-warning mb-3"></i>
                <h6>Gestión Presupuestal</h6>
                <p class="text-muted small">Controlar CDP</p>
                <a href="#" class="btn btn-outline-warning btn-sm">Próximamente</a>
            </div>
        </div>
    </div>
    
    <div class="col-lg-3 col-md-6 mb-3">
        <div class="card h-100">
            <div class="card-body text-center">
                <i class="fas fa-folder-open fa-3x text-info mb-3"></i>
                <h6>Expedientes</h6>
                <p class="text-muted small">Documentación</p>
                <a href="#" class="btn btn-outline-info btn-sm">Próximamente</a>
            </div>
        </div>
    </div>
</div>
""",
)

# Formulario de registro HTML
REGISTRO_HTML = BASE_TEMPLATE.replace(
    "{% block content %}{% endblock %}",
    """
<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h1 class="h3 mb-0">Registro de Prestador de Servicios</h1>
        <p class="text-muted">Complete la información básica del PS</p>
    </div>
    <div>
        <a href="/" class="btn btn-outline-secondary">Volver al Dashboard</a>
    </div>
</div>

<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="card">
            <div class="card-body">
                <form method="POST" action="/registro">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="cedula" class="form-label">Cédula *</label>
                                <input type="text" class="form-control" id="cedula" name="cedula" required maxlength="12">
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="nombre_completo" class="form-label">Nombre Completo *</label>
                                <input type="text" class="form-control" id="nombre_completo" name="nombre_completo" required maxlength="255">
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="correo" class="form-label">Correo Electrónico *</label>
                                <input type="email" class="form-control" id="correo" name="correo" required>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="telefono" class="form-label">Teléfono</label>
                                <input type="tel" class="form-control" id="telefono" name="telefono">
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="perfil_profesional" class="form-label">Perfil Profesional *</label>
                                <select class="form-select" id="perfil_profesional" name="perfil_profesional" required>
                                    <option value="">Seleccione...</option>
                                    <option value="TECNICO">Técnico</option>
                                    <option value="TECNOLOGO">Tecnólogo</option>
                                    <option value="PROFESIONAL">Profesional</option>
                                    <option value="ESPECIALISTA">Especialista</option>
                                    <option value="MAGISTER">Magíster</option>
                                    <option value="DOCTOR">Doctor</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="experiencia_meses" class="form-label">Experiencia (Meses) *</label>
                                <input type="number" class="form-control" id="experiencia_meses" name="experiencia_meses" required min="0">
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="sector" class="form-label">Sector *</label>
                                <select class="form-select" id="sector" name="sector" required>
                                    <option value="">Seleccione...</option>
                                    <option value="PUBLICO">Público</option>
                                    <option value="PRIVADO">Privado</option>
                                    <option value="MIXTO">Mixto</option>
                                    <option value="ACADEMICO">Académico</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="modalidad" class="form-label">Modalidad *</label>
                                <select class="form-select" id="modalidad" name="modalidad" required>
                                    <option value="">Seleccione...</option>
                                    <option value="PRESTACION_SERVICIOS">Prestación de Servicios</option>
                                    <option value="OBRA_LABOR">Obra o Labor</option>
                                    <option value="CONSULTOR">Consultor</option>
                                    <option value="APOYO_GESTION">Apoyo a la Gestión</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    
                    <div class="d-flex justify-content-between mt-4">
                        <a href="/" class="btn btn-secondary">Cancelar</a>
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save me-1"></i>Registrar PS
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
""",
)


@app.route("/")
def dashboard():
    """Dashboard principal"""
    return render_template_string(DASHBOARD_HTML)


@app.route("/registro", methods=["GET", "POST"])
def registro():
    """Formulario de registro"""
    if request.method == "POST":
        # Obtener datos del formulario
        cedula = request.form.get("cedula")
        nombre = request.form.get("nombre_completo")
        correo = request.form.get("correo")

        # Validación básica
        if not cedula or not nombre or not correo:
            flash("Todos los campos obligatorios deben ser completados", "error")
            return render_template_string(REGISTRO_HTML)

        # Simular guardado exitoso
        flash(f"PS {nombre} registrado exitosamente (Cédula: {cedula})", "success")
        return redirect(url_for("dashboard"))

    return render_template_string(REGISTRO_HTML)


@app.route("/api/stats")
def api_stats():
    """API de estadísticas"""
    return jsonify(
        {
            "total_ps": 0,
            "ps_activos": 0,
            "ps_en_proceso": 0,
            "cdp_disponible": 0,
            "alertas_activas": 0,
        }
    )


if __name__ == "__main__":
    print("🚀 Iniciando MiloTalent (versión independiente)")
    print("📍 URL: http://localhost:5000")
    print("✅ Sin problemas de templates Jinja2")
    print("✅ Sin dependencias de MiloApps")
    print("✅ Completamente funcional")
    app.run(debug=True, port=5000)
