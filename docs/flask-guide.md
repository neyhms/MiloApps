# InfoMilo - Desarrollo con Python Flask

## 🚀 **¡Tu aplicación Flask está funcionando!**

### 📱 **Accede a tu aplicación:**
- **URL principal:** http://127.0.0.1:8080
- **API de configuración:** http://127.0.0.1:8080/api/config
- **Estado del sistema:** http://127.0.0.1:8080/api/status
- **Cambiar configuración:** POST http://127.0.0.1:8080/api/switch-env

### 🐍 **Características de la aplicación Flask:**
- ✅ **Servidor Flask** con hot reload
- ✅ **Configuración dinámica** (casa/oficina/default)
- ✅ **API RESTful** para gestión de configuraciones
- ✅ **Templates HTML** con Jinja2
- ✅ **CORS habilitado** para desarrollo
- ✅ **Entorno virtual** configurado
- ✅ **Variables de entorno** con python-dotenv

### 🔧 **Comandos disponibles:**

#### **Desarrollo diario:**
```bash
# Iniciar servidor de desarrollo
C:/Users/neyhm/InfoMilo/.venv/Scripts/python.exe src/app.py

# O usando npm scripts
npm run dev

# Con Flask CLI (modo debug)
npm run dev:flask
```

#### **Gestión del proyecto:**
```bash
# Instalar dependencias
npm run install:deps

# Build para producción
npm run build

# Ejecutar tests
npm run test

# Linting con flake8
npm run lint

# Formatear código con black
npm run format
```

#### **Cambiar configuraciones:**
```bash
# Casa
npm run switch:home

# Oficina  
npm run switch:office

# O usar PowerShell directamente
.\scripts\switch-env.ps1 home
.\scripts\switch-env.ps1 office
```

### 📁 **Estructura del proyecto Flask:**
```
InfoMilo/
├── src/
│   ├── app.py              # Aplicación Flask principal
│   └── templates/
│       └── index.html      # Template principal
├── config/
│   ├── home.json          # Configuración para casa
│   ├── office.json        # Configuración para oficina
│   ├── default.json       # Configuración por defecto
│   └── active.json        # Configuración activa
├── .venv/                 # Entorno virtual Python
├── requirements.txt       # Dependencias Python
└── .env                   # Variables de entorno
```

### 🔄 **API Endpoints:**

#### **GET /** 
Página principal con interfaz web

#### **GET /api/config**
```json
{
  "environment": "office",
  "description": "Configuración para trabajo desde la oficina",
  "development": {
    "port": 8080,
    "host": "0.0.0.0",
    "debug_mode": false
  },
  "network": {
    "proxy": true,
    "proxy_url": "http://proxy.empresa.com:8080"
  }
}
```

#### **GET /api/status**
```json
{
  "status": "running",
  "environment": "office",
  "server": "Flask/Python",
  "port": 8080,
  "timestamp": "2025-10-04T17:54:00"
}
```

#### **POST /api/switch-env**
Cambiar configuración dinámicamente
```json
{
  "environment": "home"
}
```

### 🏠🏢 **Configuraciones específicas:**

#### **Casa (home.json):**
- Puerto: 3000
- Host: localhost
- Debug: Habilitado
- Proxy: Deshabilitado
- Backup: Cloud sync habilitado

#### **Oficina (office.json):**
- Puerto: 8080
- Host: 0.0.0.0 (acceso desde red)
- Debug: Deshabilitado (seguridad)
- Proxy: Habilitado para red corporativa
- Backup: Solo local y unidad de red

### 🛠️ **Desarrollo avanzado:**

#### **Agregar nuevas rutas:**
```python
@app.route('/api/nueva-ruta')
def nueva_ruta():
    return jsonify({'mensaje': 'Nueva funcionalidad'})
```

#### **Usar configuración en el código:**
```python
def mi_funcion():
    config = app.config_manager.config
    puerto = config['development']['port']
    debug = config['development']['debug_mode']
    # Tu lógica aquí
```

#### **Agregar nuevas plantillas:**
1. Crear archivo en `src/templates/`
2. Usar `render_template('mi_template.html')`
3. Pasar datos con `render_template('template.html', datos=mi_data)`

### 🔐 **Variables de entorno:**
Edita `.env` para configuraciones sensibles:
```env
FLASK_SECRET_KEY=tu_clave_secreta
DATABASE_URL=sqlite:///infomilo.db
API_KEY=tu_api_key
```

### 📦 **Despliegue:**
```bash
# Build para producción
npm run build

# Los archivos estarán en dist/
cd dist
pip install -r requirements.txt
python app.py
```

### 🐛 **Debug y desarrollo:**
- Los logs aparecen en la terminal
- Cambios en templates se reflejan automáticamente
- Para debug profundo, cambia `debug_mode: true` en la configuración
- Usa `print()` para debug rápido o el módulo `logging` para producción

### 🎉 **¡Tu aplicación Flask está lista!**
- Interfaz web moderna y responsive
- Configuración flexible para casa/oficina
- API RESTful completamente funcional
- Entorno de desarrollo optimizado
- Estructura escalable y mantenible
