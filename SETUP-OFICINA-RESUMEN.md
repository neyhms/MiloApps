# 🎯 RESUMEN: Setup Primera Vez en Oficina

## 📋 ¿QUÉ NECESITAS?

**Software imprescindible:**
- ✅ **Python 3.11+** - [python.org](https://python.org)
- ✅ **Git** - [git-scm.com](https://git-scm.com) 

**Verificar instalación:**
```powershell
python --version
git --version
```

**Obtener el proyecto:**
- 🔗 **Repositorio Git**: `https://github.com/neyhms/InfoMilo.git` (una vez configurado)
- 💾 **Transferencia manual**: USB/OneDrive/carpeta compartida
- 📖 **Ver guía completa**: `docs/git-setup-guide.md`

---

## 🚀 OPCIONES DE SETUP (ELIGE UNA)

### **Opción 1: Doble Click (MÁS FÁCIL)**
1. Doble click en: `setup-oficina-simple.bat`
2. ¡Listo!

### **Opción 2: Script Express PowerShell**
```powershell
.\scripts\setup-express.ps1
```

### **Opción 3: Script Completo**
```powershell
.\scripts\setup-office.ps1
```

### **Opción 4: Una Línea**
```powershell
python -m venv .venv && .venv\Scripts\pip install -r requirements.txt && copy config\office.json config\active.json
```

---

## ✅ VERIFICAR QUE FUNCIONA

```powershell
# Iniciar aplicación
.venv\Scripts\python.exe src\app.py

# Debería mostrar:
# * Running on http://0.0.0.0:8080
```

**Abrir navegador:** http://localhost:8080  
**Debería mostrar:** "🏢 OFICINA"

---

## 🎯 USO DIARIO

Una vez configurado, para trabajo diario:

```powershell
# Método 1: Script maestro (RECOMENDADO)
.\scripts\work-manager.ps1
# Elegir opción 3: "Iniciar trabajo en oficina"

# Método 2: Directo
.venv\Scripts\python.exe src\app.py
```

---

## 📚 DOCUMENTACIÓN COMPLETA

- **📖 Setup detallado:** `SETUP-PRIMERA-VEZ-OFICINA.md`
- **📋 Checklist oficina:** `CHECKLIST-OFICINA.md`
- **🚀 Inicio rápido:** `OFICINA-QUICK-START.md`
- **🔧 Guía oficina:** `docs/office-setup-guide.md`

---

## 🆘 ¿PROBLEMAS?

### Python no encontrado:
- Instalar desde [python.org](https://python.org)
- Marcar "Add to PATH" durante instalación

### Error permisos PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Puerto 8080 ocupado:
```powershell
netstat -ano | findstr :8080
taskkill /PID [número] /F
```

---

## 🎉 ¡YA ESTÁS LISTO!

**Con cualquiera de estos métodos tendrás InfoMilo funcionando en tu oficina en menos de 5 minutos.**
