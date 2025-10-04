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
echo ✅ ¡SETUP BÁSICO COMPLETADO!
echo.
echo � CONFIGURAR GITHUB (Recomendado para sincronización):
echo    .\scripts\work-manager.ps1
echo    Opción 8: Configurar GitHub primera vez
echo.
echo �🚀 OPCIONES PARA INICIAR:
echo    MÉTODO 1 (Recomendado): .\scripts\work-manager.ps1
echo    MÉTODO 2 (Directo): .venv\Scripts\python.exe src\app.py
echo.
echo 🌐 URL: http://localhost:8080
echo.
echo 💡 Para trabajo diario usa el script maestro:
echo    .\scripts\work-manager.ps1
echo.
pause
