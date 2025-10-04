# Script para INICIAR trabajo desde OFICINA
# Ejecutar al comenzar el día de trabajo en la oficina

Write-Host "🏢 INICIANDO TRABAJO DESDE OFICINA..." -ForegroundColor Blue
Write-Host "=====================================" -ForegroundColor Blue
Write-Host ""

# Paso 1: Verificar requisitos
Write-Host "🔍 1. Verificando requisitos..." -ForegroundColor Yellow
$pythonOk = Get-Command python -ErrorAction SilentlyContinue
$gitOk = Get-Command git -ErrorAction SilentlyContinue

if ($pythonOk) {
    Write-Host "✅ Python disponible" -ForegroundColor Green
} else {
    Write-Host "❌ Python no encontrado - instalar desde python.org" -ForegroundColor Red
    exit 1
}

if ($gitOk) {
    Write-Host "✅ Git disponible" -ForegroundColor Green
} else {
    Write-Host "❌ Git no encontrado - instalar desde git-scm.com" -ForegroundColor Red
    exit 1
}

# Paso 2: Sincronizar cambios
Write-Host "📥 2. Sincronizando cambios desde casa..." -ForegroundColor Yellow
git pull origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Cambios sincronizados correctamente" -ForegroundColor Green
} else {
    Write-Host "⚠️  Problemas sincronizando - revisar manualmente" -ForegroundColor Yellow
}

# Paso 3: Configurar para oficina
Write-Host "🏢 3. Configurando entorno de OFICINA..." -ForegroundColor Yellow
Copy-Item -Path "config\office.json" -Destination "config\active.json" -Force

# Verificar configuración
$config = Get-Content "config\active.json" | ConvertFrom-Json
if ($config.environment -eq "office") {
    Write-Host "✅ Configuración de OFICINA activada" -ForegroundColor Green
} else {
    Write-Host "❌ Error en configuración" -ForegroundColor Red
}

# Paso 4: Configurar Git corporativo
Write-Host "🏢 4. Configurando Git corporativo..." -ForegroundColor Yellow
$currentEmail = git config user.email 2>$null
if ($currentEmail -notlike "*@empresa.com") {
    Write-Host "   💡 Tip: Configurar email corporativo con:" -ForegroundColor Gray
    Write-Host "   git config user.email tu.email@empresa.com" -ForegroundColor Gray
}

# Paso 5: Preparar entorno Python
Write-Host "🐍 5. Preparando entorno Python..." -ForegroundColor Yellow
if (!(Test-Path ".venv")) {
    Write-Host "📦 Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv .venv
}

if (Test-Path ".venv\Scripts\python.exe") {
    Write-Host "✅ Entorno virtual listo" -ForegroundColor Green
    
    # Instalar/actualizar dependencias
    Write-Host "📋 Instalando dependencias..." -ForegroundColor Yellow
    & .venv\Scripts\pip.exe install -r requirements.txt --quiet
    Write-Host "✅ Dependencias instaladas" -ForegroundColor Green
} else {
    Write-Host "❌ Error creando entorno virtual" -ForegroundColor Red
    exit 1
}

# Paso 6: Configurar proxy si es necesario
Write-Host "🔗 6. Verificando configuración de red..." -ForegroundColor Yellow
if ($config.network.proxy) {
    Write-Host "✅ Proxy corporativo configurado" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Sin proxy configurado" -ForegroundColor Gray
}

# Paso 7: Iniciar aplicación
Write-Host "🚀 7. Iniciando aplicación Flask..." -ForegroundColor Yellow
Write-Host ""
Write-Host "🎉 ¡OFICINA CONFIGURADA!" -ForegroundColor Blue
Write-Host "📋 INFORMACIÓN:" -ForegroundColor Cyan
Write-Host "   🌐 URL: http://localhost:8080" -ForegroundColor White
Write-Host "   🏢 Entorno: OFICINA" -ForegroundColor White
Write-Host "   🔒 Debug: DESHABILITADO" -ForegroundColor White
Write-Host "   🔗 Proxy: CORPORATIVO" -ForegroundColor White
Write-Host "   💾 Backup: RED CORPORATIVA" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Iniciando servidor..." -ForegroundColor Blue

# Activar entorno e iniciar
& .venv\Scripts\activate
Start-Process "http://localhost:8080"
& .venv\Scripts\python.exe src\app.py
