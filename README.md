# MiloApps - Proyecto Flexible para Trabajo Remoto

Un proyecto diseñado para facilitar el desarrollo tanto desde casa como desde la oficina, con configuraciones flexibles y herramientas de colaboración.

## 🏠🏢 **Trabajo Multi-Ubicación**

MiloApps está específicamente diseñado para trabajar seamlessly desde diferentes ubicaciones:

### **🏠 Desde Casa:**
- Puerto: 3000
- Debug: Habilitado  
- Backup: Cloud sync
- Proxy: Deshabilitado

### **🏢 Desde Oficina:**
- Puerto: 8080
- Debug: Deshabilitado (seguridad)
- Backup: Red corporativa
- Proxy: Corporativo habilitado

### **🚀 Setup Rápido en Nuevo Ordenador:**
```bash
# 1. Clonar proyecto
git clone https://github.com/neyhms/MiloApps.git
cd MiloApps

# 2. Setup automático para oficina
.\scripts\setup-office.ps1

# 3. O setup manual
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.\scripts\switch-env.ps1 office
python src\app.py
```

### **🚀 Setup Primera Vez en Oficina:**

**Requisitos:** Python 3.11+, Git

```powershell
# MÉTODO 1: Setup automático (Recomendado)
.\scripts\setup-office.ps1

# MÉTODO 2: Setup express (3 comandos)
.\scripts\setup-express.ps1

# MÉTODO 3: Setup manual
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
copy config\office.json config\active.json
```

**📖 Guía completa:** Ver `SETUP-PRIMERA-VEZ-OFICINA.md`

### **🔧 Setup Manual Básico:**
```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/InfoMilo.git
cd InfoMilo

# 2. Crear y activar el entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Linux o macOS
.\.venv\Scripts\activate   # En Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar el entorno
cp config/default.json config/active.json
```

## 🏠 Características Principales

- **Estructura modular**: Organización clara y escalable
- **Configuración flexible**: Adaptable a diferentes entornos de trabajo
- **Documentación completa**: Fácil onboarding para nuevos desarrolladores
- **Herramientas de colaboración**: Configuradas para trabajo en equipo
- **Cross-platform**: Compatible con Windows, macOS y Linux

## 📁 Estructura del Proyecto

```
InfoMilo/
├── .github/                 # Configuraciones de GitHub y Copilot
│   └── copilot-instructions.md
├── .vscode/                 # Configuraciones de VS Code
│   ├── settings.json
│   ├── tasks.json
│   └── extensions.json
├── config/                  # Configuraciones por ambiente
│   ├── home.json
│   ├── office.json
│   └── default.json
├── docs/                    # Documentación del proyecto
│   ├── setup-guide.md
│   └── development-guide.md
├── scripts/                 # Scripts de automatización
│   ├── setup.ps1
│   └── deploy.ps1
├── src/                     # Código fuente
│   └── main.js
├── .env.example            # Plantilla de variables de entorno
├── .gitignore              # Archivos ignorados por Git
└── README.md               # Este archivo
```

## 🚀 Inicio Rápido

### Configuración Inicial
1. Clona el repositorio
2. Copia `.env.example` a `.env` y configura tus variables
3. Ejecuta el script de setup: `.\scripts\setup.ps1`
4. Selecciona tu perfil de trabajo (casa/oficina)

### Comandos Disponibles
- `npm run dev`: Inicia el entorno de desarrollo
- `npm run build`: Construye el proyecto
- `npm run test`: Ejecuta las pruebas
- `npm run deploy`: Despliega el proyecto

## 🔧 Configuración por Ambiente

El proyecto incluye configuraciones predefinidas para diferentes entornos:

- **Casa**: Configuración para trabajo desde casa
- **Oficina**: Configuración para trabajo desde la oficina
- **Por defecto**: Configuración genérica

## 📖 Documentación

- [Guía de Configuración](docs/setup-guide.md)
- [Guía de Desarrollo](docs/development-guide.md)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Añade nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crea un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## 🆘 Soporte

Si tienes problemas o preguntas, por favor:
1. Revisa la documentación en la carpeta `docs/`
2. Busca en los issues existentes
3. Crea un nuevo issue si es necesario
