"""
MiloTalent Blueprint - Versión simplificada sin CSRF
"""

from flask import (
    Blueprint,
    render_template_string,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
)
from flask_login import login_required, current_user

# Crear blueprint sin CSRF
milotalent_bp = Blueprint("milotalent", __name__, url_prefix="/milotalent")

# HTML simplificado sin formularios complejos
DASHBOARD_SIMPLE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MiloTalent - Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .stat-card { 
            border-radius: 15px; 
            padding: 1.5rem; 
            margin-bottom: 1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .stat-value { font-size: 2.5rem; font-weight: bold; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <div class="container">
            <a class="navbar-brand text-white" href="/dashboard">
                <i class="fas fa-home me-2"></i>MiloApps
            </a>
            <div class="navbar-nav ms-auto">
                <span class="nav-link text-white">
                    <i class="fas fa-user me-1"></i>{{ username }}
                </span>
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h1 class="h3 mb-0">
                    <i class="fas fa-users-cog me-2"></i>MiloTalent - Dashboard
                </h1>
                <p class="text-muted">Sistema de Contratación de Prestadores de Servicios</p>
            </div>
            <div>
                <a href="/milotalent/registro" class="btn btn-primary btn-lg">
                    <i class="fas fa-plus me-2"></i>Registrar Nuevo PS
                </a>
            </div>
        </div>

        <div class="row mb-4">
            <div class="col-lg-3 col-md-6">
                <div class="card bg-primary text-white stat-card">
                    <div class="card-body text-center">
                        <div class="stat-value">0</div>
                        <div><i class="fas fa-users me-2"></i>Total PS Registrados</div>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="card bg-success text-white stat-card">
                    <div class="card-body text-center">
                        <div class="stat-value">0</div>
                        <div><i class="fas fa-handshake me-2"></i>Contratos Activos</div>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="card bg-warning text-white stat-card">
                    <div class="card-body text-center">
                        <div class="stat-value">0</div>
                        <div><i class="fas fa-clock me-2"></i>En Proceso</div>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="card bg-info text-white stat-card">
                    <div class="card-body text-center">
                        <div class="stat-value">0</div>
                        <div><i class="fas fa-check-circle me-2"></i>Completados</div>
                    </div>
                </div>
            </div>
        </div>

        <div style="background: white; border-radius: 15px; padding: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4><i class="fas fa-list me-2"></i>Prestadores de Servicios</h4>
            <div class="text-center py-5">
                <i class="fas fa-users fa-4x text-muted mb-3"></i>
                <h5 class="text-muted">Sistema Listo para Usar</h5>
                <p class="text-muted">MiloTalent ha sido integrado exitosamente en MiloApps</p>
                <div class="mt-4">
                    <a href="/milotalent/registro" class="btn btn-primary me-2">
                        <i class="fas fa-plus me-1"></i>Registrar Prestador
                    </a>
                    <a href="/dashboard" class="btn btn-outline-secondary">
                        <i class="fas fa-arrow-left me-1"></i>Volver al Dashboard
                    </a>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

REGISTRO_SIMPLE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MiloTalent - Registro</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .form-container {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <div class="container">
            <a class="navbar-brand text-white" href="/dashboard">
                <i class="fas fa-home me-2"></i>MiloApps
            </a>
            <div class="navbar-nav ms-auto">
                <span class="nav-link text-white">
                    <i class="fas fa-user me-1"></i>{{ username }}
                </span>
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="form-container">
                    <div class="text-center mb-4">
                        <h2><i class="fas fa-user-plus me-2"></i>Registro de Prestador de Servicios</h2>
                        <p class="text-muted">Complete el formulario para registrar un nuevo prestador</p>
                    </div>
                    
                    {% if message %}
                        <div class="alert alert-{{ message_type }} alert-dismissible fade show">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endif %}
                    
                    <form method="POST" action="/milotalent/registro">
                        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label">
                                        <i class="fas fa-user me-1"></i>Nombre *
                                    </label>
                                    <input type="text" class="form-control" name="nombre" required>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label">
                                        <i class="fas fa-user me-1"></i>Apellido *
                                    </label>
                                    <input type="text" class="form-control" name="apellido" required>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label">
                                        <i class="fas fa-envelope me-1"></i>Email *
                                    </label>
                                    <input type="email" class="form-control" name="email" required>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label">
                                        <i class="fas fa-phone me-1"></i>Teléfono *
                                    </label>
                                    <input type="tel" class="form-control" name="telefono" required>
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">
                                <i class="fas fa-briefcase me-1"></i>Servicios que Ofrece *
                            </label>
                            <div class="row">
                                <div class="col-md-4">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="Plomería" name="servicios">
                                        <label class="form-check-label">Plomería</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="Electricidad" name="servicios">
                                        <label class="form-check-label">Electricidad</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="Carpintería" name="servicios">
                                        <label class="form-check-label">Carpintería</label>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="Pintura" name="servicios">
                                        <label class="form-check-label">Pintura</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="Jardinería" name="servicios">
                                        <label class="form-check-label">Jardinería</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="Limpieza" name="servicios">
                                        <label class="form-check-label">Limpieza</label>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="Albañilería" name="servicios">
                                        <label class="form-check-label">Albañilería</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="Herrería" name="servicios">
                                        <label class="form-check-label">Herrería</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="Otros" name="servicios">
                                        <label class="form-check-label">Otros</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                            <a href="/milotalent" class="btn btn-secondary btn-lg me-md-2">
                                <i class="fas fa-arrow-left me-2"></i>Cancelar
                            </a>
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-save me-2"></i>Registrar Prestador
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""


@milotalent_bp.route("/")
@login_required
def dashboard():
    """Dashboard principal de MiloTalent"""
    username = current_user.username if current_user.is_authenticated else "Usuario"
    return render_template_string(DASHBOARD_SIMPLE, username=username)


@milotalent_bp.route("/registro", methods=["GET", "POST"])
@login_required
def registro():
    """Formulario de registro de prestadores"""
    username = current_user.username if current_user.is_authenticated else "Usuario"
    message = None
    message_type = "success"

    if request.method == "POST":
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        email = request.form.get("email")
        telefono = request.form.get("telefono")
        servicios = request.form.getlist("servicios")

        if not all([nombre, apellido, email, telefono]) or not servicios:
            message = "Todos los campos obligatorios deben completarse"
            message_type = "danger"
        else:
            message = f"Prestador {nombre} {apellido} registrado exitosamente"
            message_type = "success"

    return render_template_string(
        REGISTRO_SIMPLE, username=username, message=message, message_type=message_type
    )


@milotalent_bp.route("/api/stats")
@login_required
def api_stats():
    """API para estadísticas"""
    return jsonify(
        {
            "total_ps": 0,
            "contratos_activos": 0,
            "en_proceso": 0,
            "completados_mes": 0,
            "success": True,
        }
    )
