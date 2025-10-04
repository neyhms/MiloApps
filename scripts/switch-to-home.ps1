# Script automático para volver a trabajar desde casa
# Ejecutar después de haber trabajado en la oficina

Write-Host "🏠 Configurando InfoMilo para trabajo desde CASA..." -ForegroundColor Green
Write-Host ""

# Verificar que estamos en el directorio correcto
if (!(Test-Path "config\home.json")) {
    Write-Host "❌ No se encuentra config\home.json" -ForegroundColor Red
    Write-Host "   Asegúrate de estar en el directorio raíz del proyecto InfoMilo" -ForegroundColor Yellow
    exit 1
}

# Sincronizar cambios de la oficina
Write-Host "📥 Sincronizando cambios de la oficina..." -ForegroundColor Yellow
git pull origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ Problemas sincronizando con Git" -ForegroundColor Yellow
    Write-Host "   Revisa si hay conflictos o problemas de red" -ForegroundColor Gray
} else {
    Write-Host "✅ Cambios sincronizados correctamente" -ForegroundColor Green
}

# Cambiar a configuración de casa
Write-Host "⚙️ Activando configuración de CASA..." -ForegroundColor Yellow
Copy-Item -Path "config\home.json" -Destination "config\active.json" -Force

if (Test-Path "config\active.json") {
    $config = Get-Content "config\active.json" | ConvertFrom-Json
    if ($config.environment -eq "home") {
        Write-Host "✅ Configuración de casa activada" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Problema activando configuración de casa" -ForegroundColor Yellow
    }
}

# Configurar Git para uso personal
Write-Host "🔗 Configurando Git para uso personal..." -ForegroundColor Yellow
$currentEmail = git config user.email 2>$null
if ($currentEmail -like "*@empresa.com") {
    Write-Host "   Cambiando de email corporativo a personal..." -ForegroundColor Gray
    Write-Host "   Recuerda configurar: git config user.email tu.email@personal.com" -ForegroundColor Gray
} else {
    Write-Host "✅ Email de Git configurado para uso personal" -ForegroundColor Green
}

# Verificar entorno virtual
Write-Host "🐍 Verificando entorno Python..." -ForegroundColor Yellow
if (Test-Path ".venv\Scripts\python.exe") {
    Write-Host "✅ Entorno virtual encontrado" -ForegroundColor Green
    
    # Verificar dependencias
    $packages = & .venv\Scripts\pip.exe list 2>$null
    if ($packages -match "Flask") {
        Write-Host "✅ Dependencias de Flask disponibles" -ForegroundColor Green
    } else {
        Write-Host "📦 Instalando dependencias..." -ForegroundColor Yellow
        & .venv\Scripts\pip.exe install -r requirements.txt
    }
} else {
    Write-Host "❌ Entorno virtual no encontrado" -ForegroundColor Red
    Write-Host "   Crear con: python -m venv .venv" -ForegroundColor Yellow
}

# Mostrar resumen de configuración
Write-Host ""
Write-Host "📋 CONFIGURACIÓN ACTUAL:" -ForegroundColor Cyan
Write-Host "   🏠 Entorno: CASA" -ForegroundColor White
Write-Host "   🌐 Puerto: 3000" -ForegroundColor White
Write-Host "   🖥️  Host: localhost" -ForegroundColor White
Write-Host "   🐛 Debug: HABILITADO" -ForegroundColor White
Write-Host "   ☁️  Backup: Cloud sync" -ForegroundColor White
Write-Host "   🔗 Proxy: DESHABILITADO" -ForegroundColor White

Write-Host ""
Write-Host "🎉 ¡Configuración de casa completada!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Siguientes pasos:" -ForegroundColor Cyan
Write-Host "   1. Activar entorno: .venv\Scripts\activate" -ForegroundColor White
Write-Host "   2. Iniciar app: python src\app.py" -ForegroundColor White
Write-Host "   3. Abrir: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "✨ La aplicación debería mostrar '🏠 CASA' en la interfaz" -ForegroundColor Green
Write-Host ""
