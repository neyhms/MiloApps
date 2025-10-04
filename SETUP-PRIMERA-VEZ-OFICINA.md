# 🏢 SETUP PRIMERA VEZ - ORDENADOR OFICINA

## 📋 CHECKLIST RÁPIDO ANTES DE EMPEZAR

### ✅ Software que DEBE estar instalado:
- [ ] **Git** - [Descargar aquí](https://git-scm.com/)
- [ ] **Python 3.11+** - [Descargar aquí](https://www.python.org/downloads/)
- [ ] **VS Code** (opcional) - [Descargar aquí](https://code.visualstudio.com/)

### 🔍 Verificar instalaciones:
```powershell
# Abrir PowerShell y verificar:
git --version
python --version
pip --version
```

---

## 🚀 MÉTODO 1: SETUP AUTOMÁTICO (RECOMENDADO)

### Paso 1: Obtener el proyecto
```powershell
# Opción A: Desde repositorio Git (SI tienes el código en GitHub/GitLab)
git clone https://github.com/tu-usuario/InfoMilo.git
cd InfoMilo

# Opción B: Desde USB/OneDrive (SI copias la carpeta manualmente)
# 1. Copia toda la carpeta InfoMilo al escritorio de la oficina
# 2. Abre PowerShell en esa carpeta
```

### Paso 2: Ejecutar setup automático
```powershell
# ¡UN SOLO COMANDO LO HACE TODO!
.\scripts\setup-office.ps1
```

**¿Qué hace este comando?**
- ✅ Verifica Python instalado
- ✅ Crea entorno virtual (.venv)
- ✅ Instala todas las dependencias Flask
- ✅ Configura automáticamente para oficina
- ✅ Configura Git con email corporativo
- ✅ ¡Listo para trabajar!

### Paso 3: Empezar a trabajar
```powershell
# Ejecutar el script maestro
.\scripts\work-manager.ps1
# Seleccionar: 3 (Iniciar trabajo en oficina)
```

---

## 🔧 MÉTODO 2: SETUP MANUAL (SI FALLA EL AUTOMÁTICO)

### Paso 1: Crear entorno virtual
```powershell
# Crear .venv
python -m venv .venv

# Activar entorno virtual
.venv\Scripts\activate

# Verificar que está activo (debería aparecer (.venv) en el prompt)
```

### Paso 2: Instalar dependencias
```powershell
# Instalar paquetes Python
pip install -r requirements.txt

# Verificar instalación
pip list
# Deberías ver: Flask, flask-cors, python-dotenv, requests
```

### Paso 3: Configurar para oficina
```powershell
# Cambiar a configuración oficina
copy config\office.json config\active.json

# Verificar configuración
type config\active.json
```

### Paso 4: Configurar Git (OPCIONAL)
```powershell
# Solo si vas a hacer commits desde oficina
git config user.name "Tu Nombre"
git config user.email "tu.email@empresa.com"
```

### Paso 5: Probar que funciona
```powershell
# Iniciar aplicación
python src\app.py

# Debería mostrar: "Running on http://0.0.0.0:8080"
# Abrir navegador: http://localhost:8080
```

---

## 🌐 CONFIGURACIONES ESPECÍFICAS DE OFICINA

### Si hay PROXY corporativo:
```powershell
# Configurar proxy para pip
pip install --proxy http://proxy.empresa.com:8080 -r requirements.txt

# Configurar proxy para git
git config --global http.proxy http://proxy.empresa.com:8080
```

### Si hay restricciones de PowerShell:
```powershell
# Ejecutar como administrador si es necesario
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🎯 COMANDO SUPER RÁPIDO (TODO EN UNO)

```powershell
# COPIA Y PEGA ESTO EN POWERSHELL:
python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt && copy config\office.json config\active.json && echo "✅ LISTO! Ejecuta: python src\app.py"
```

---

## ✅ VERIFICAR QUE TODO FUNCIONA

### Test 1: Verificar entorno
```powershell
# Activar entorno virtual
.venv\Scripts\activate

# Debería aparecer (.venv) en el prompt
```

### Test 2: Verificar dependencias
```powershell
pip list | findstr Flask
# Debería mostrar: Flask 3.1.2
```

### Test 3: Verificar configuración
```powershell
type config\active.json | findstr office
# Debería mostrar: "environment": "office"
```

### Test 4: Probar aplicación
```powershell
python src\app.py
# Debería iniciar en puerto 8080
# Ctrl+C para detener
```

### Test 5: Usar script maestro
```powershell
.\scripts\work-manager.ps1
# Debería mostrar menú con "OFICINA" como configuración actual
```

---

## 🚨 TROUBLESHOOTING COMÚN

### Error: "python no reconocido"
```powershell
# Verificar que Python está en PATH
# Reinstalar Python marcando "Add to PATH"
```

### Error: "pip no reconocido"
```powershell
# Usar python -m pip en lugar de pip
python -m pip install -r requirements.txt
```

### Error: "No se puede ejecutar scripts"
```powershell
# Cambiar política de ejecución
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "Puerto 8080 ocupado"
```powershell
# Ver qué proceso usa el puerto
netstat -ano | findstr :8080
# Matar proceso si es necesario
taskkill /PID [número_pid] /F
```

---

## 📁 ESTRUCTURA QUE DEBERÍAS TENER

Después del setup, tu carpeta debería verse así:
```
InfoMilo/
├── .venv/          ✅ (Entorno virtual creado)
├── config/
│   └── active.json ✅ (Configuración oficina activa)
├── src/
│   └── app.py      ✅ (Aplicación Flask)
├── scripts/        ✅ (Scripts automáticos)
└── requirements.txt ✅ (Dependencias)
```

---

## 🎉 ¡YA ESTÁS LISTO!

Una vez completado el setup, para trabajar diariamente solo necesitas:

### Rutina diaria oficina:
```powershell
# 1. Abrir PowerShell en carpeta InfoMilo
cd ruta\a\InfoMilo

# 2. Ejecutar script maestro
.\scripts\work-manager.ps1

# 3. Seleccionar opción 3: "Iniciar trabajo en oficina"
# 4. ¡Trabajar! La app estará en http://localhost:8080
```

---

## 📞 ¿NECESITAS AYUDA?

Si algo no funciona:
1. Verifica que Python y Git están instalados
2. Ejecuta los comandos paso a paso
3. Revisa los mensajes de error
4. Consulta la documentación en `docs/`

**¡Con esta guía deberías estar trabajando en menos de 10 minutos!** 🚀
