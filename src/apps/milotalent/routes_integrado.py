"""
MiloTalent Blueprint - Sistema de Contratación de Prestadores de Servicios
Integrado con MiloApps usando render_template_string para evitar errores de Jinja2
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
from flask_wtf.csrf import generate_csrf

# Crear blueprint
milotalent_bp = Blueprint("milotalent", __name__, url_prefix="/milotalent")

# Template base HTML que funciona sin errores
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}MiloTalent - MiloApps{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .navbar { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .navbar-brand { color: white !important; font-weight: bold; }
        .navbar-nav .nav-link { color: rgba(255,255,255,0.9) !important; }
        .navbar-nav .nav-link:hover { color: white !important; }
        .stat-card { 
            border-radius: 15px; 
            padding: 1.5rem; 
            margin-bottom: 1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-value { font-size: 2.5rem; font-weight: bold; }
        .btn-primary { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
        }
        .table-container {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .form-container {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        body { background-color: #f8f9fa; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg">
        <div class="container">
            <a class="navbar-brand" href="/dashboard">
                <i class="fas fa-home me-2"></i>MiloApps
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/milotalent">
                    <i class="fas fa-users-cog me-1"></i>MiloTalent
                </a>
                <span class="nav-link text-white">
                    <i class="fas fa-user me-1"></i>{{ current_user.username if current_user.is_authenticated else 'Usuario' }}
                </span>
            </div>
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
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
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
        <a href="/milotalent/registro" class="btn btn-primary btn-lg">
            <i class="fas fa-plus me-2"></i>Registrar Nuevo PS
        </a>
    </div>
</div>

<div class="row mb-4">
    <div class="col-lg-3 col-md-6">
        <div class="card bg-primary text-white stat-card">
            <div class="card-body text-center">
                <div class="stat-value">{{ stats.total_ps }}</div>
                <div><i class="fas fa-users me-2"></i>Total PS Registrados</div>
            </div>
        </div>
    </div>
    <div class="col-lg-3 col-md-6">
        <div class="card bg-success text-white stat-card">
            <div class="card-body text-center">
                <div class="stat-value">{{ stats.contratos_activos }}</div>
                <div><i class="fas fa-handshake me-2"></i>Contratos Activos</div>
            </div>
        </div>
    </div>
    <div class="col-lg-3 col-md-6">
        <div class="card bg-warning text-white stat-card">
            <div class="card-body text-center">
                <div class="stat-value">{{ stats.en_proceso }}</div>
                <div><i class="fas fa-clock me-2"></i>En Proceso</div>
            </div>
        </div>
    </div>
    <div class="col-lg-3 col-md-6">
        <div class="card bg-info text-white stat-card">
            <div class="card-body text-center">
                <div class="stat-value">{{ stats.completados_mes }}</div>
                <div><i class="fas fa-check-circle me-2"></i>Completados este mes</div>
            </div>
        </div>
    </div>
</div>

<div class="table-container">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h4><i class="fas fa-list me-2"></i>Prestadores de Servicios Registrados</h4>
        <div class="input-group" style="width: 300px;">
            <span class="input-group-text"><i class="fas fa-search"></i></span>
            <input type="text" class="form-control" placeholder="Buscar prestador..." id="searchInput">
        </div>
    </div>
    
    <div class="table-responsive">
        <table class="table table-hover">
            <thead class="table-dark">
                <tr>
                    <th><i class="fas fa-id-badge me-1"></i>ID</th>
                    <th><i class="fas fa-user me-1"></i>Nombre Completo</th>
                    <th><i class="fas fa-envelope me-1"></i>Email</th>
                    <th><i class="fas fa-phone me-1"></i>Teléfono</th>
                    <th><i class="fas fa-briefcase me-1"></i>Servicios</th>
                    <th><i class="fas fa-calendar me-1"></i>Fecha Registro</th>
                    <th><i class="fas fa-cogs me-1"></i>Acciones</th>
                </tr>
            </thead>
            <tbody id="prestadoresTable">
                {% if prestadores %}
                    {% for ps in prestadores %}
                    <tr>
                        <td><span class="badge bg-primary">{{ ps.id }}</span></td>
                        <td><strong>{{ ps.nombre }} {{ ps.apellido }}</strong></td>
                        <td>{{ ps.email }}</td>
                        <td>{{ ps.telefono }}</td>
                        <td>
                            <span class="badge bg-secondary">{{ ps.servicios | length }} servicios</span>
                        </td>
                        <td>{{ ps.fecha_registro.strftime('%d/%m/%Y') }}</td>
                        <td>
                            <div class="btn-group btn-group-sm">
                                <button class="btn btn-outline-primary" title="Ver detalles">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <button class="btn btn-outline-warning" title="Editar">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button class="btn btn-outline-info" title="Contratar">
                                    <i class="fas fa-handshake"></i>
                                </button>
                            </div>
                        </td>
                    </tr>
                    {% endfor %}
                {% else %}
                    <tr>
                        <td colspan="7" class="text-center text-muted py-4">
                            <i class="fas fa-users fa-3x mb-3 d-block"></i>
                            <h5>No hay prestadores registrados aún</h5>
                            <p>Comienza registrando tu primer prestador de servicios</p>
                            <a href="/milotalent/registro" class="btn btn-primary">
                                <i class="fas fa-plus me-2"></i>Registrar Primer PS
                            </a>
                        </td>
                    </tr>
                {% endif %}
            </tbody>
        </table>
    </div>
</div>

<script>
// Búsqueda en tiempo real
document.getElementById('searchInput').addEventListener('keyup', function() {
    const filter = this.value.toLowerCase();
    const rows = document.querySelectorAll('#prestadoresTable tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(filter) ? '' : 'none';
    });
});
</script>
""",
)

# Formulario de registro HTML
REGISTRO_HTML = BASE_TEMPLATE.replace(
    "{% block content %}{% endblock %}",
    """
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="form-container">
            <div class="text-center mb-4">
                <h2><i class="fas fa-user-plus me-2"></i>Registro de Prestador de Servicios</h2>
                <p class="text-muted">Complete el formulario para registrar un nuevo prestador</p>
            </div>
            
            <form method="POST" action="/milotalent/registro" id="registroForm">
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="nombre" class="form-label">
                                <i class="fas fa-user me-1"></i>Nombre *
                            </label>
                            <input type="text" class="form-control" id="nombre" name="nombre" required>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="apellido" class="form-label">
                                <i class="fas fa-user me-1"></i>Apellido *
                            </label>
                            <input type="text" class="form-control" id="apellido" name="apellido" required>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="email" class="form-label">
                                <i class="fas fa-envelope me-1"></i>Email *
                            </label>
                            <input type="email" class="form-control" id="email" name="email" required>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="telefono" class="form-label">
                                <i class="fas fa-phone me-1"></i>Teléfono *
                            </label>
                            <input type="tel" class="form-control" id="telefono" name="telefono" required>
                        </div>
                    </div>
                </div>
                
                <div class="mb-3">
                    <label for="direccion" class="form-label">
                        <i class="fas fa-map-marker-alt me-1"></i>Dirección
                    </label>
                    <textarea class="form-control" id="direccion" name="direccion" rows="2"></textarea>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="documento_tipo" class="form-label">
                                <i class="fas fa-id-card me-1"></i>Tipo de Documento *
                            </label>
                            <select class="form-select" id="documento_tipo" name="documento_tipo" required>
                                <option value="">Seleccionar...</option>
                                <option value="DNI">DNI</option>
                                <option value="CUIT">CUIT</option>
                                <option value="CUIL">CUIL</option>
                                <option value="Pasaporte">Pasaporte</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="documento_numero" class="form-label">
                                <i class="fas fa-hashtag me-1"></i>Número de Documento *
                            </label>
                            <input type="text" class="form-control" id="documento_numero" name="documento_numero" required>
                        </div>
                    </div>
                </div>
                
                <div class="mb-3">
                    <label for="servicios" class="form-label">
                        <i class="fas fa-briefcase me-1"></i>Servicios que Ofrece *
                    </label>
                    <div class="row">
                        <div class="col-md-4">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="Plomería" id="servicio1" name="servicios">
                                <label class="form-check-label" for="servicio1">Plomería</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="Electricidad" id="servicio2" name="servicios">
                                <label class="form-check-label" for="servicio2">Electricidad</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="Carpintería" id="servicio3" name="servicios">
                                <label class="form-check-label" for="servicio3">Carpintería</label>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="Pintura" id="servicio4" name="servicios">
                                <label class="form-check-label" for="servicio4">Pintura</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="Jardinería" id="servicio5" name="servicios">
                                <label class="form-check-label" for="servicio5">Jardinería</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="Limpieza" id="servicio6" name="servicios">
                                <label class="form-check-label" for="servicio6">Limpieza</label>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="Albañilería" id="servicio7" name="servicios">
                                <label class="form-check-label" for="servicio7">Albañilería</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="Herrería" id="servicio8" name="servicios">
                                <label class="form-check-label" for="servicio8">Herrería</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="Otros" id="servicio9" name="servicios">
                                <label class="form-check-label" for="servicio9">Otros</label>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="mb-3">
                    <label for="experiencia" class="form-label">
                        <i class="fas fa-star me-1"></i>Años de Experiencia
                    </label>
                    <select class="form-select" id="experiencia" name="experiencia">
                        <option value="">Seleccionar...</option>
                        <option value="0-1">Menos de 1 año</option>
                        <option value="1-3">1 a 3 años</option>
                        <option value="3-5">3 a 5 años</option>
                        <option value="5-10">5 a 10 años</option>
                        <option value="10+">Más de 10 años</option>
                    </select>
                </div>
                
                <div class="mb-3">
                    <label for="descripcion" class="form-label">
                        <i class="fas fa-info-circle me-1"></i>Descripción Adicional
                    </label>
                    <textarea class="form-control" id="descripcion" name="descripcion" rows="3" 
                              placeholder="Describa brevemente su experiencia y servicios especializados..."></textarea>
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

<script>
// Validación del formulario
document.getElementById('registroForm').addEventListener('submit', function(e) {
    const servicios = document.querySelectorAll('input[name="servicios"]:checked');
    if (servicios.length === 0) {
        e.preventDefault();
        alert('Debe seleccionar al menos un servicio');
        return false;
    }
});
</script>
""",
)


# Rutas del blueprint
@milotalent_bp.route("/")
@login_required
def dashboard():
    """Dashboard principal de MiloTalent"""
    # Datos simulados para mostrar funcionalidad
    stats = {
        "total_ps": 0,
        "contratos_activos": 0,
        "en_proceso": 0,
        "completados_mes": 0,
    }

    prestadores = []  # Lista vacía por ahora

    return render_template_string(DASHBOARD_HTML, stats=stats, prestadores=prestadores)


@milotalent_bp.route("/registro", methods=["GET", "POST"])
@login_required
def registro():
    """Formulario de registro de prestadores"""
    if request.method == "POST":
        # Procesar el formulario
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        email = request.form.get("email")
        telefono = request.form.get("telefono")
        servicios = request.form.getlist("servicios")

        # Validación básica
        if not all([nombre, apellido, email, telefono]) or not servicios:
            flash("Todos los campos obligatorios deben completarse", "error")
            return render_template_string(REGISTRO_HTML)

        # Aquí se guardará en la base de datos
        # Por ahora solo mostramos un mensaje de éxito
        flash(f"Prestador {nombre} {apellido} registrado exitosamente", "success")
        return redirect(url_for("milotalent.dashboard"))

    return render_template_string(REGISTRO_HTML)


@milotalent_bp.route("/api/stats")
@login_required
def api_stats():
    """API para obtener estadísticas de MiloTalent"""
    stats = {
        "total_ps": 0,
        "contratos_activos": 0,
        "en_proceso": 0,
        "completados_mes": 0,
        "nuevos_esta_semana": 0,
        "promedio_calificacion": 0.0,
    }
    return jsonify(stats)


@milotalent_bp.route("/api/prestadores")
@login_required
def api_prestadores():
    """API para obtener lista de prestadores"""
    prestadores = []  # Lista vacía por ahora
    return jsonify(
        {"prestadores": prestadores, "total": len(prestadores), "success": True}
    )
