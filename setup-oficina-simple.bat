@echo off
echo 🏢 InfoMilo - Setup Oficina ULTRA RAPIDO
echo =====================================
echo.

echo 📦 Creando entorno virtual...
python -m venv .venv
if %errorlevel% neq 0 (
    echo ❌ Error: Instalar Python desde https://python.org
    pause
    exit /b 1
)

echo 📋 Instalando dependencias...
.venv\Scripts\pip.exe install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Error instalando. Verificar internet.
    pause
    exit /b 1
)

echo ⚙️ Configurando oficina...
copy config\office.json config\active.json >nul

echo.
echo ✅ ¡LISTO!
echo 🚀 Ejecutar: .venv\Scripts\python.exe src\app.py
echo 🌐 URL: http://localhost:8080
echo.
pause
