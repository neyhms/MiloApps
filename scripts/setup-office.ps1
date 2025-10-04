# Script de configuración automática para oficina
# Ejecutar este script en el ordenador de la oficina para configurar todo

Write-Host "🏢 Configurando InfoMilo para OFICINA..." -ForegroundColor Blue
Write-Host ""

# Verificar Python
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python no encontrado. Descargar desde https://python.org" -ForegroundColor Red
    Write-Host "   Reiniciar este script después de instalar Python." -ForegroundColor Yellow
    exit 1
}

# Verificar Git
try {
    $gitVersion = git --version 2>$null
    Write-Host "✅ Git encontrado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git no encontrado. Descargar desde https://git-scm.com" -ForegroundColor Red
    exit 1
}

# Crear entorno virtual si no existe
if (!(Test-Path ".venv")) {
    Write-Host "📦 Creando entorno virtual Python..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error creando entorno virtual" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Entorno virtual creado" -ForegroundColor Green
} else {
    Write-Host "📦 Entorno virtual ya existe" -ForegroundColor Green
}

# Activar entorno virtual e instalar dependencias
Write-Host "📋 Instalando dependencias Python..." -ForegroundColor Yellow
& .venv\Scripts\python.exe -m pip install --upgrade pip
& .venv\Scripts\pip.exe install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencias instaladas correctamente" -ForegroundColor Green
} else {
    Write-Host "❌ Error instalando dependencias" -ForegroundColor Red
    Write-Host "   Verificar conexión a internet o configuración de proxy" -ForegroundColor Yellow
}

# Configurar para oficina
Write-Host "⚙️ Activando configuración de oficina..." -ForegroundColor Yellow
if (Test-Path "config\office.json") {
    Copy-Item -Path "config\office.json" -Destination "config\active.json" -Force
    Write-Host "✅ Configuración de oficina activada" -ForegroundColor Green
} else {
    Write-Host "⚠️ Archivo config\office.json no encontrado" -ForegroundColor Yellow
}

# Configurar Git para oficina
Write-Host "🔗 Configurando Git para oficina..." -ForegroundColor Yellow
$currentEmail = git config user.email 2>$null
if ($currentEmail -notlike "*@empresa.com") {
    Write-Host "   Configurar email corporativo:" -ForegroundColor Gray
    Write-Host "   git config user.email tu.email@empresa.com" -ForegroundColor Gray
}

# Crear directorios necesarios
$directories = @("temp", "logs", "dist", "build")
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "📁 Creado directorio: $dir" -ForegroundColor Gray
    }
}

# Crear .env si no existe
if (!(Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item -Path ".env.example" -Destination ".env"
        Write-Host "📝 Archivo .env creado desde ejemplo" -ForegroundColor Yellow
        Write-Host "   Revisar y personalizar variables de entorno" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "🎉 ¡Configuración de oficina completada!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Siguiente pasos:" -ForegroundColor Cyan
Write-Host "   1. Revisar configuración: type config\active.json" -ForegroundColor White
Write-Host "   2. Personalizar .env si es necesario" -ForegroundColor White
Write-Host "   3. Iniciar aplicación: .\.venv\Scripts\python.exe src\app.py" -ForegroundColor White
Write-Host ""
Write-Host "🌐 La aplicación estará disponible en:" -ForegroundColor Cyan
Write-Host "   http://localhost:8080 (configuración de oficina)" -ForegroundColor White
Write-Host ""
Write-Host "🔄 Para gestión diaria:" -ForegroundColor Cyan
Write-Host "   Script maestro: .\scripts\work-manager.ps1" -ForegroundColor White
Write-Host ""
Write-Host "🔗 Para sincronización automática con GitHub:" -ForegroundColor Magenta
if (Test-Path ".git") {
    $hasRemote = git remote -v 2>$null
    if (![string]::IsNullOrEmpty($hasRemote)) {
        Write-Host "   ✅ GitHub ya configurado" -ForegroundColor Green
        git remote -v | Select-Object -First 1
    } else {
        Write-Host "   ⚠️ Configurar GitHub: Opción 8 en script maestro" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ⚠️ Inicializar Git: Opción 8 en script maestro" -ForegroundColor Yellow
}
Write-Host ""
