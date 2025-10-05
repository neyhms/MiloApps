# Script para INICIAR trabajo desde CASA
# Ejecutar al comenzar el día de trabajo en casa

Write-Host "🏠 INICIANDO TRABAJO DESDE CASA..." -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""

# Cambiar al directorio del proyecto
Set-Location -Path $PSScriptRoot\..

# Paso 1: Sincronizar cambios desde GitHub
Write-Host "📥 1. Sincronizando cambios desde GitHub..." -ForegroundColor Yellow
if (Test-Path ".git") {
    try {
        git pull origin main
        Write-Host "✅ Cambios sincronizados desde GitHub" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Error de conexión - continuando sin sincronizar" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️ No es repositorio Git" -ForegroundColor Yellow
}

# Paso 2: Configurar para casa
Write-Host "🏠 2. Configurando entorno de CASA..." -ForegroundColor Yellow
Copy-Item -Path "config\home.json" -Destination "config\active.json" -Force
Write-Host "✅ Configuración de CASA activada" -ForegroundColor Green

# Paso 3: Preparar entorno Python
Write-Host "🐍 3. Preparando entorno Python..." -ForegroundColor Yellow
if (Test-Path ".venv\Scripts\python.exe") {
    Write-Host "✅ Entorno virtual encontrado" -ForegroundColor Green
} else {
    Write-Host "📦 Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv .venv
    .venv\Scripts\pip.exe install -r requirements.txt
}

# Información del sistema
Write-Host ""
Write-Host "🎉 ¡CASA CONFIGURADA!" -ForegroundColor Green
Write-Host "📋 INFORMACIÓN:" -ForegroundColor Cyan
Write-Host "   🌐 URL: http://localhost:3000" -ForegroundColor White
Write-Host "   🏠 Entorno: CASA" -ForegroundColor White
Write-Host "   🐛 Debug: HABILITADO" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Para iniciar MiloApps:" -ForegroundColor Green
Write-Host "   .venv\Scripts\python.exe src\app.py" -ForegroundColor Yellow
