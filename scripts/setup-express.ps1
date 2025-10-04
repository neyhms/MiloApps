# 🚀 SETUP EXPRESS - 3 COMANDOS Y LISTO

Write-Host "🏢 InfoMilo - Setup Express Oficina" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Paso 1: Crear y activar entorno virtual
Write-Host "📦 Paso 1/3: Creando entorno virtual..." -ForegroundColor Yellow
python -m venv .venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error: Python no encontrado o falló creación de .venv" -ForegroundColor Red
    Write-Host "   Instalar Python desde: https://python.org" -ForegroundColor Yellow
    exit 1
}

# Paso 2: Instalar dependencias
Write-Host "📋 Paso 2/3: Instalando Flask y dependencias..." -ForegroundColor Yellow
& .venv\Scripts\pip.exe install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error instalando dependencias" -ForegroundColor Red
    Write-Host "   Verificar conexión a internet" -ForegroundColor Yellow
    exit 1
}

# Paso 3: Configurar para oficina
Write-Host "⚙️ Paso 3/3: Configurando para oficina..." -ForegroundColor Yellow
Copy-Item -Path "config\office.json" -Destination "config\active.json" -Force

# Finalizado
Write-Host ""
Write-Host "✅ ¡SETUP COMPLETADO!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Para iniciar aplicación:" -ForegroundColor Cyan
Write-Host "   .\.venv\Scripts\python.exe src\app.py" -ForegroundColor White
Write-Host ""
Write-Host "🌐 URL: http://localhost:8080" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔄 Script maestro (Recomendado):" -ForegroundColor Cyan
Write-Host "   .\scripts\work-manager.ps1" -ForegroundColor White
Write-Host ""
Write-Host "🔗 Para sincronización automática casa ↔ oficina:" -ForegroundColor Magenta
Write-Host "   Ejecutar script maestro → Opción 8: Configurar GitHub" -ForegroundColor White
