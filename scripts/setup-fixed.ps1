# InfoMilo Setup Script
# Script para configurar el entorno de desarrollo

param(
    [string]$Environment = "default"
)

Write-Host "🚀 Configurando InfoMilo para trabajo remoto..." -ForegroundColor Green
Write-Host ""

# Verificar si Node.js está instalado
try {
    $nodeVersion = node --version 2>$null
    Write-Host "✅ Node.js encontrado: $nodeVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Node.js no encontrado. Por favor instalalo desde https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Verificar si Git está instalado
try {
    $gitVersion = git --version 2>$null
    Write-Host "✅ Git encontrado: $gitVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Git no encontrado. Por favor instalalo desde https://git-scm.com/" -ForegroundColor Red
    exit 1
}

# Crear directorios necesarios
$directories = @("temp", "logs", "dist", "build")
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "📁 Creado directorio: $dir" -ForegroundColor Yellow
    }
}

# Copiar archivo de configuración según el entorno
$configFile = "config/$Environment.json"
if (Test-Path $configFile) {
    Copy-Item -Path $configFile -Destination "config/active.json" -Force
    Write-Host "⚙️  Configuración '$Environment' activada" -ForegroundColor Cyan
}
else {
    Copy-Item -Path "config/default.json" -Destination "config/active.json" -Force
    Write-Host "⚙️  Usando configuración por defecto" -ForegroundColor Cyan
}

# Crear archivo .env si no existe
if (!(Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item -Path ".env.example" -Destination ".env"
        Write-Host "📝 Archivo .env creado desde .env.example" -ForegroundColor Yellow
    }
}

# Instalar dependencias si existe package.json
if (Test-Path "package.json") {
    Write-Host "📦 Instalando dependencias..." -ForegroundColor Cyan
    npm install
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dependencias instaladas correctamente" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Error al instalar dependencias" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🎉 ¡Configuración completada!" -ForegroundColor Green
Write-Host ""
Write-Host "Comandos disponibles:" -ForegroundColor Cyan
Write-Host "  - Cambiar a casa:    .\scripts\switch-env.ps1 home" -ForegroundColor White
Write-Host "  - Cambiar a oficina: .\scripts\switch-env.ps1 office" -ForegroundColor White  
Write-Host "  - Iniciar desarrollo: npm run dev" -ForegroundColor White
Write-Host "  - Construir proyecto: npm run build" -ForegroundColor White
Write-Host ""
