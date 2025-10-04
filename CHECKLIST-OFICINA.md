# ✅ CHECKLIST - TRABAJAR DESDE LA OFICINA

## 📥 ANTES DE IR A LA OFICINA (Casa)

- [ ] Hacer commit de todos los cambios
- [ ] Push al repositorio remoto: `git push origin main`
- [ ] Verificar que no hay archivos importantes sin commitear
- [ ] Opcional: Crear branch específico para trabajo de oficina

```bash
git add .
git commit -m "sync: preparando para trabajo en oficina"
git push origin main
```

---

## 🏢 AL LLEGAR A LA OFICINA (Primer día)

### Setup inicial:
- [ ] Verificar Python instalado: `python --version`
- [ ] Verificar Git instalado: `git --version`
- [ ] Clonar repositorio: `git clone [tu-repo] InfoMilo`
- [ ] Entrar al directorio: `cd InfoMilo`
- [ ] Ejecutar setup: `.\scripts\setup-office.ps1`
- [ ] Verificar aplicación: `python src\app.py`
- [ ] Abrir navegador: http://localhost:8080
- [ ] Confirmar que muestra "🏢 OFICINA"

### Configurar Git para oficina:
- [ ] `git config user.name "Tu Nombre"`
- [ ] `git config user.email "tu.email@empresa.com"`

---

## 🔄 RUTINA DIARIA EN OFICINA

### 🌅 Al llegar cada día:
- [ ] `git pull origin main`
- [ ] `.venv\Scripts\activate`
- [ ] `.\scripts\switch-env.ps1 office`
- [ ] `python src\app.py`
- [ ] Verificar: http://localhost:8080

### 💻 Durante el trabajo:
- [ ] Commits frecuentes: `git commit -m "descripción"`
- [ ] Usar configuración de oficina (puerto 8080)
- [ ] Verificar que proxy funciona si es necesario

### 🌙 Al terminar el día:
- [ ] `git add .`
- [ ] `git commit -m "trabajo oficina: [resumen del día]"`
- [ ] `git push origin main`
- [ ] Cerrar aplicación (Ctrl+C)

---

## 🏠 AL VOLVER A CASA

### Setup en casa:
- [ ] `git pull origin main` (obtener cambios de oficina)
- [ ] `.\scripts\switch-env.ps1 home`
- [ ] `python src\app.py`
- [ ] Verificar: http://localhost:3000
- [ ] Confirmar que muestra "🏠 CASA"

---

## 🚨 PROBLEMAS COMUNES

### ❌ "Python no encontrado":
- [ ] Instalar Python desde python.org
- [ ] Reiniciar terminal/VS Code
- [ ] Verificar PATH del sistema

### ❌ "Puerto 8080 ocupado":
- [ ] Cambiar puerto en `config/office.json`
- [ ] O usar: `netstat -ano | findstr :8080` para ver qué lo usa

### ❌ "Error instalando paquetes":
- [ ] Verificar conexión a internet
- [ ] Configurar proxy si es necesario:
  ```bash
  pip install --proxy http://proxy.empresa.com:8080 -r requirements.txt
  ```

### ❌ "Git no funciona":
- [ ] Configurar proxy Git:
  ```bash
  git config --global http.proxy http://proxy.empresa.com:8080
  ```

---

## ✨ VERIFICACIÓN FINAL

Todo funciona correctamente si:
- [ ] ✅ `python --version` muestra Python 3.11+
- [ ] ✅ `.venv\Scripts\pip list` muestra Flask instalado
- [ ] ✅ `type config\active.json` muestra configuración de oficina
- [ ] ✅ http://localhost:8080 muestra la aplicación
- [ ] ✅ La interfaz muestra "🏢 OFICINA"
- [ ] ✅ `git status` no muestra errores

---

## 📱 URLs DE REFERENCIA

- **App:** http://localhost:8080 (oficina) / http://localhost:3000 (casa)
- **Config:** http://localhost:8080/api/config
- **Status:** http://localhost:8080/api/status

---

## 📖 DOCUMENTACIÓN COMPLETA

- `docs/office-setup-guide.md` - Guía detallada
- `docs/flask-guide.md` - Desarrollo con Flask
- `OFICINA-QUICK-START.md` - Comandos rápidos

---

**💡 TIP:** Guarda este checklist en tu teléfono o imprímelo para tener referencia rápida en la oficina.
