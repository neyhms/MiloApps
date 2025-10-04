# Guía para Trabajar desde la Oficina - Otro Ordenador

## 🏢 **Configuración en el Ordenador de la Oficina**

### 📋 **Requisitos Previos**
Antes de empezar, asegúrate de tener instalado en el ordenador de la oficina:

#### **Software esencial:**
- **Git** - [Descargar](https://git-scm.com/)
- **Python 3.11+** - [Descargar](https://www.python.org/downloads/)
- **Visual Studio Code** - [Descargar](https://code.visualstudio.com/)
- **Node.js** (opcional, para npm scripts) - [Descargar](https://nodejs.org/)

#### **Verificar instalaciones:**
```bash
# Verificar Git
git --version

# Verificar Python
python --version
# o
python3 --version

# Verificar pip
pip --version
```

---

## 📥 **Paso 1: Clonar el Proyecto**

### **Opción A: Desde repositorio Git (Recomendado)**
```bash
# Clonar tu repositorio
git clone https://github.com/tu-usuario/InfoMilo.git
cd InfoMilo

# O si usas SSH
git clone git@github.com:tu-usuario/InfoMilo.git
cd InfoMilo
```

### **Opción B: Desde archivo comprimido**
1. Comprime tu carpeta InfoMilo en casa
2. Sube a cloud (OneDrive, Google Drive, etc.)
3. Descarga y descomprime en la oficina

---

## 🐍 **Paso 2: Configurar Entorno Python**

### **Crear entorno virtual:**
```bash
# En Windows (oficina)
python -m venv .venv

# Activar entorno virtual
.venv\Scripts\activate

# En Linux/Mac (si aplica)
python3 -m venv .venv
source .venv/bin/activate
```

### **Instalar dependencias:**
```bash
# Instalar paquetes desde requirements.txt
pip install -r requirements.txt

# Verificar instalación
pip list
```

---

## ⚙️ **Paso 3: Configurar para Oficina**

### **Activar configuración de oficina:**
```bash
# Windows PowerShell
.\scripts\switch-env.ps1 office

# O manualmente
copy config\office.json config\active.json
```

### **Verificar configuración:**
```bash
# Ver configuración activa
type config\active.json

# O en Python
python -c "import json; print(json.load(open('config/active.json')))"
```

---

## 🔧 **Paso 4: Configurar VS Code**

### **Instalar extensiones automáticamente:**
VS Code detectará el archivo `.vscode/extensions.json` y te sugerirá instalar:
- Python
- Flask
- GitHub Copilot
- PowerShell
- Material Icon Theme

### **Configurar intérprete Python:**
1. `Ctrl+Shift+P`
2. "Python: Select Interpreter"
3. Seleccionar: `.\\.venv\\Scripts\\python.exe`

---

## 🌐 **Paso 5: Iniciar la Aplicación**

### **Método 1: VS Code Tasks**
```
Ctrl+Shift+P → Tasks: Run Task → Start Development Server
```

### **Método 2: Terminal**
```bash
# Activar entorno virtual (si no está activo)
.venv\Scripts\activate

# Iniciar aplicación Flask
python src\app.py

# O usar npm scripts (si tienes Node.js)
npm run dev
```

### **Verificar funcionamiento:**
- Abrir: http://localhost:8080 (configuración oficina)
- Debería mostrar "🏢 OFICINA" en la interfaz

---

## 🔄 **Paso 6: Sincronización Diaria**

### **Al llegar a la oficina:**
```bash
# Actualizar código
git pull origin main

# Activar entorno virtual
.venv\Scripts\activate

# Cambiar a configuración oficina
.\scripts\switch-env.ps1 office

# Iniciar desarrollo
python src\app.py
```

### **Al final del día:**
```bash
# Guardar cambios
git add .
git commit -m "Trabajo desde oficina - [descripción]"
git push origin main
```

---

## 🔐 **Paso 7: Configuraciones Específicas de Oficina**

### **Variables de entorno (.env):**
```env
# Configuración específica de oficina
NODE_ENV=office
FLASK_ENV=production
HOST=0.0.0.0
PORT=8080

# Proxy corporativo (si aplica)
HTTP_PROXY=http://proxy.empresa.com:8080
HTTPS_PROXY=http://proxy.empresa.com:8080

# Base de datos de oficina
DATABASE_URL=postgresql://user:pass@db-office.empresa.com:5432/infomilo

# APIs internas
INTERNAL_API_URL=https://api-interna.empresa.com
API_KEY_OFFICE=tu_api_key_corporativa
```

### **Configuración de Git:**
```bash
# Configurar Git para oficina
git config user.name "Tu Nombre"
git config user.email "tu.email@empresa.com"

# Ver configuración
git config --list
```

---

## 🚀 **Script de Setup Automático para Oficina**

Crea este archivo como `scripts/setup-office.ps1`:

```powershell
# Setup automático para oficina
Write-Host "🏢 Configurando InfoMilo para OFICINA..." -ForegroundColor Blue

# Verificar Python
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "✅ Python encontrado" -ForegroundColor Green
} else {
    Write-Host "❌ Python no encontrado. Instalar desde python.org" -ForegroundColor Red
    exit 1
}

# Crear entorno virtual si no existe
if (!(Test-Path ".venv")) {
    Write-Host "📦 Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activar entorno virtual
Write-Host "🔧 Activando entorno virtual..." -ForegroundColor Yellow
& .venv\Scripts\Activate.ps1

# Instalar dependencias
Write-Host "📋 Instalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt

# Configurar para oficina
Write-Host "⚙️ Activando configuración de oficina..." -ForegroundColor Yellow
Copy-Item -Path "config\office.json" -Destination "config\active.json" -Force

# Configurar Git
Write-Host "🔗 Configurando Git..." -ForegroundColor Yellow
git config user.email "tu.email@empresa.com"

Write-Host "✅ ¡Configuración de oficina completada!" -ForegroundColor Green
Write-Host "🚀 Ejecuta: python src\app.py" -ForegroundColor Cyan
```

---

## 📱 **Uso en el día a día**

### **Rutina matutina en oficina:**
1. **Llegar y actualizar:**
   ```bash
   git pull origin main
   ```

2. **Activar entorno:**
   ```bash
   .venv\Scripts\activate
   ```

3. **Cambiar a configuración oficina:**
   ```bash
   .\scripts\switch-env.ps1 office
   ```

4. **Iniciar desarrollo:**
   ```bash
   python src\app.py
   ```

### **Durante el desarrollo:**
- La aplicación se ejecuta en puerto 8080 (oficina)
- Proxy corporativo configurado automáticamente
- Debug deshabilitado por seguridad
- Backup solo en unidad de red corporativa

### **Al finalizar el día:**
```bash
# Guardar trabajo
git add .
git commit -m "feat: [descripción del trabajo]"
git push origin main

# Opcional: crear branch para trabajo específico
git checkout -b feature/trabajo-oficina
git push origin feature/trabajo-oficina
```

---

## 🔧 **Troubleshooting Común**

### **Error de proxy:**
```bash
# Configurar proxy para pip
pip install --proxy http://proxy.empresa.com:8080 -r requirements.txt

# Configurar proxy para git
git config --global http.proxy http://proxy.empresa.com:8080
```

### **Error de puerto ocupado:**
```bash
# Ver qué proceso usa el puerto
netstat -ano | findstr :8080

# Cambiar puerto en config/office.json si es necesario
```

### **Error de permisos:**
```bash
# Ejecutar PowerShell como administrador si es necesario
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📊 **Diferencias Casa vs Oficina**

| Aspecto | Casa | Oficina |
|---------|------|---------|
| **Puerto** | 3000 | 8080 |
| **Host** | localhost | 0.0.0.0 |
| **Proxy** | No | Sí |
| **Debug** | Habilitado | Deshabilitado |
| **Backup** | Cloud | Red corporativa |
| **Git Email** | personal | corporativo |
| **VPN** | Opcional | Requerida |

---

## 🎯 **Checklist para Oficina**

- [ ] Python instalado
- [ ] Git configurado
- [ ] Proyecto clonado
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] Configuración de oficina activa
- [ ] VS Code configurado
- [ ] Aplicación funcionando en puerto 8080
- [ ] Proxy configurado (si aplica)
- [ ] Git email corporativo configurado

---

## 🚀 **Setup de Una Sola Vez**

Guarda este comando para setup rápido:

```bash
# Un comando para configurar todo
git clone [tu-repo] && cd InfoMilo && python -m venv .venv && .venv\Scripts\pip install -r requirements.txt && .\scripts\switch-env.ps1 office && python src\app.py
```

Con esta guía, podrás trabajar seamlessly desde cualquier ordenador en la oficina manteniendo toda la funcionalidad y configuraciones específicas del entorno corporativo! 🏢✨
