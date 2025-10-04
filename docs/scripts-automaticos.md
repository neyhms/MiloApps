# 🚀 SCRIPTS AUTOMÁTICOS - INFOMILO

## 📋 **SCRIPTS DISPONIBLES**

### 🎯 **Script Maestro (Recomendado)**
```bash
.\scripts\work-manager.ps1
```
**Menú interactivo con todas las opciones**

---

## 🏠 **SCRIPTS PARA CASA**

### **Iniciar trabajo en casa:**
```bash
.\scripts\start-work-home.ps1
```
**Hace automáticamente:**
- ✅ `git pull origin main`
- ✅ Activa configuración de casa
- ✅ Configura Git personal
- ✅ Prepara entorno Python
- ✅ Inicia aplicación en http://localhost:3000

### **Terminar trabajo en casa:**
```bash
.\scripts\end-work-home.ps1
```
**Hace automáticamente:**
- ✅ `git add . && git commit`
- ✅ `git push origin main`
- ✅ Genera resumen del día
- ✅ Limpia procesos
- ✅ Prepara para próximo trabajo

---

## 🏢 **SCRIPTS PARA OFICINA**

### **Iniciar trabajo en oficina:**
```bash
.\scripts\start-work-office.ps1
```
**Hace automáticamente:**
- ✅ Verifica requisitos (Python, Git)
- ✅ `git pull origin main`
- ✅ Activa configuración de oficina
- ✅ Configura Git corporativo
- ✅ Configura proxy si es necesario
- ✅ Inicia aplicación en http://localhost:8080

### **Terminar trabajo en oficina:**
```bash
.\scripts\end-work-office.ps1
```
**Hace automáticamente:**
- ✅ `git add . && git commit`
- ✅ `git push origin main`
- ✅ Crea backup corporativo
- ✅ Genera resumen del día
- ✅ Limpia entorno

---

## ⚡ **USO DIARIO SIMPLIFICADO**

### **🌅 Al empezar el día:**
```bash
# En casa
.\scripts\start-work-home.ps1

# En oficina
.\scripts\start-work-office.ps1
```

### **🌙 Al terminar el día:**
```bash
# En casa
.\scripts\end-work-home.ps1

# En oficina
.\scripts\end-work-office.ps1
```

---

## 🔄 **FLUJO COMPLETO SEMANAL**

### **Lunes (Casa → Oficina):**
```bash
# En casa por la mañana
.\scripts\start-work-home.ps1
# ... trabajar ...
.\scripts\end-work-home.ps1

# En oficina por la tarde
.\scripts\start-work-office.ps1
# ... trabajar ...
.\scripts\end-work-office.ps1
```

### **Martes (Oficina → Casa):**
```bash
# En oficina por la mañana
.\scripts\start-work-office.ps1
# ... trabajar ...
.\scripts\end-work-office.ps1

# En casa por la tarde
.\scripts\start-work-home.ps1
# ... trabajar ...
.\scripts\end-work-home.ps1
```

---

## 🛠️ **SCRIPTS AUXILIARES**

### **Solo cambiar configuración:**
```bash
# A casa
.\scripts\switch-env.ps1 home

# A oficina
.\scripts\switch-env.ps1 office
```

### **Setup inicial oficina:**
```bash
.\scripts\setup-office.ps1
```

### **Volver a casa después de oficina:**
```bash
.\scripts\switch-to-home.ps1
```

---

## 🚨 **SOLUCIÓN DE PROBLEMAS**

### **Si un script falla:**
1. **Ejecutar manualmente los pasos**
2. **Usar el script maestro:** `.\scripts\work-manager.ps1`
3. **Ver opción 7 (estado del proyecto)**

### **Comandos de emergencia:**
```bash
# Forzar sincronización
git reset --hard origin/main

# Recrear entorno virtual
rmdir /s .venv
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt

# Cambio manual de configuración
copy config\home.json config\active.json
copy config\office.json config\active.json
```

---

## 📊 **VENTAJAS DE LOS SCRIPTS**

✅ **Automatización completa** - Un comando hace todo  
✅ **Sin errores humanos** - No olvidas pasos  
✅ **Configuración consistente** - Siempre igual  
✅ **Backup automático** - Nunca pierdes trabajo  
✅ **Commits automáticos** - Historial organizado  
✅ **Detección de errores** - Te avisa si algo falla  
✅ **Resumen del trabajo** - Sabes qué hiciste  

---

## 🎯 **RECOMENDACIÓN**

### **Usa el script maestro:**
```bash
.\scripts\work-manager.ps1
```

**Es un menú interactivo que te guía por todas las opciones disponibles y detecta tu configuración actual automáticamente.**

---

¡Con estos scripts, cambiar entre casa y oficina es tan fácil como ejecutar un comando! 🏠🏢✨
