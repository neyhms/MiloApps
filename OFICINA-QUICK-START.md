# 🏢 GUÍA RÁPIDA - TRABAJAR DESDE LA OFICINA

## ⚡ SETUP INICIAL (Una sola vez)

### 1️⃣ Clonar proyecto:
```bash
git clone https://github.com/tu-usuario/InfoMilo.git
cd InfoMilo
```

### 2️⃣ Ejecutar setup automático:
```bash
.\scripts\setup-office.ps1
```

### 3️⃣ Si el script falla, manual:
```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.\scripts\switch-env.ps1 office
```

---

## 🔄 RUTINA DIARIA

### 🌅 AL LLEGAR (5 comandos):
```bash
git pull origin main
.venv\Scripts\activate
.\scripts\switch-env.ps1 office
python src\app.py
# Abrir: http://localhost:8080
```

### 🌙 AL SALIR (3 comandos):
```bash
git add .
git commit -m "trabajo oficina: [descripción]"
git push origin main
```

---

## 🚨 PROBLEMAS COMUNES

### Puerto ocupado:
- Cambiar en `config/office.json`: `"port": 8081`

### Error proxy:
```bash
pip install --proxy http://proxy.empresa.com:8080 -r requirements.txt
```

### Python no encontrado:
- Instalar desde python.org
- Verificar: `python --version`

---

## 📞 COMANDO DE EMERGENCIA

Si algo no funciona, ejecutar todo de una vez:
```bash
python -m venv .venv && .venv\Scripts\pip install flask python-dotenv flask-cors && copy config\office.json config\active.json && .venv\Scripts\python src\app.py
```

---

## 📱 URLs IMPORTANTES

- **App principal:** http://localhost:8080
- **API config:** http://localhost:8080/api/config  
- **API status:** http://localhost:8080/api/status

---

## ⚙️ CONFIGURACIONES OFICINA

- Puerto: **8080** (no 3000)
- Host: **0.0.0.0** (acceso red)
- Debug: **OFF** (seguridad)
- Proxy: **ON** (corporativo)

---

## 📋 VERIFICAR TODO OK

```bash
# 1. Python funciona
python --version

# 2. Dependencias instaladas  
.venv\Scripts\pip list

# 3. Configuración activa
type config\active.json

# 4. App iniciada
# Ver mensaje: "🏢 OFICINA" en http://localhost:8080
```

---

## 🆘 CONTACTO

- Documentación completa: `docs/office-setup-guide.md`
- Problemas: Crear issue en GitHub
- Setup Flask: `docs/flask-guide.md`
